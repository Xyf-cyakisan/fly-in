from __future__ import annotations

import multiprocessing as mp
import time
from pathlib import Path

import pytest

from source.model.Graph import Graph
from source.parser.MapConfig import MapConfig

ROOT_DIR = Path(__file__).resolve().parent
MAPS_DIR = ROOT_DIR / "maps"
DEFAULT_TIMEOUT_SECONDS = 20
RESULTS: list[dict[str, str]] = []


def _discover_maps() -> list[Path]:
    return sorted(path for path in MAPS_DIR.rglob("*.txt") if path.is_file())


def _run_map_worker(map_path: str, result_queue: mp.Queue) -> None:
    try:
        map_config = MapConfig.parse(map_path)
        graph = Graph(map_config)
        _, turns = graph.run_simulation()
    except Exception as error:  # pragma: no cover - reported in parent process
        result_queue.put(("error", type(error).__name__, str(error)))
    else:
        result_queue.put(("ok", str(turns), ""))


def _run_map_with_timeout(
    map_path: Path, timeout_seconds: int
) -> dict[str, str]:
    result_queue: mp.Queue = mp.Queue()
    process = mp.Process(
        target=_run_map_worker,
        args=(str(map_path), result_queue),
        daemon=True,
    )
    start_time = time.monotonic()
    process.start()
    process.join(timeout_seconds)

    if process.is_alive():
        process.terminate()
        process.join()
        return {
            "map": str(map_path.relative_to(ROOT_DIR)),
            "status": "timeout",
            "tours": "-",
            "details": f"> {timeout_seconds}s",
            "elapsed": f"{time.monotonic() - start_time:.2f}s",
        }

    if result_queue.empty():
        return {
            "map": str(map_path.relative_to(ROOT_DIR)),
            "status": "error",
            "tours": "-",
            "details": "no result returned",
            "elapsed": f"{time.monotonic() - start_time:.2f}s",
        }

    status, value, details = result_queue.get()
    elapsed = f"{time.monotonic() - start_time:.2f}s"
    if status == "ok":
        return {
            "map": str(map_path.relative_to(ROOT_DIR)),
            "status": "ok",
            "tours": value,
            "details": "",
            "elapsed": elapsed,
        }

    return {
        "map": str(map_path.relative_to(ROOT_DIR)),
        "status": "error",
        "tours": "-",
        "details": f"{value}: {details}",
        "elapsed": elapsed,
    }


def _format_table(rows: list[dict[str, str]]) -> str:
    headers = ("Map", "Tours", "Status", "Elapsed")
    widths = [len(header) for header in headers]
    for row in rows:
        values = (row["map"], row["tours"], row["status"], row["elapsed"])
        for index, value in enumerate(values):
            widths[index] = max(widths[index], len(value))

    def format_row(values: tuple[str, str, str, str]) -> str:
        return (
            "| "
            + " | ".join(
                value.ljust(widths[index])
                for index, value in enumerate(values)
            )
            + " |"
        )

    separator = "| " + " | ".join("-" * width for width in widths) + " |"
    lines = [format_row(headers), separator]
    lines.extend(
        format_row((row["map"], row["tours"], row["status"], row["elapsed"]))
        for row in rows
    )
    return "\n".join(lines)


@pytest.fixture(scope="session", autouse=True)
def _print_summary_when_all_pass() -> None:
    yield
    if RESULTS and all(row["status"] == "ok" for row in RESULTS):
        print("\n" + _format_table(RESULTS))


@pytest.mark.parametrize(
    "map_path", _discover_maps(), ids=lambda path: path.stem
)
def test_all_maps_finish_without_infinite_loop(map_path: Path) -> None:
    result = _run_map_with_timeout(map_path, DEFAULT_TIMEOUT_SECONDS)
    RESULTS.append(result)
    assert result["status"] == "ok", (
        f"{result['map']} failed after {result['elapsed']}: "
        f"{result['status']} ({result['details']})"
    )
