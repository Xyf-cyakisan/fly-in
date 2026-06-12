.SILENT:

install:
	poetry config virtualenvs.in-project true
	poetry install

clean:
	rm -rf */*/__pycache__
	rm -rf */__pycache__
	rm -rf __pycache__
	rm -rf */*/.mypy_cache
	rm -rf */.mypy_cache
	rm -rf .mypy_cache
	rm -rf */*/.pytest_cache
	rm -rf */.pytest_cache
	rm -rf .pytest_cache

fclean: clean
	rm -rf .venv
	rm -rf poetry.lock

run: install
	. .venv/bin/activate ; python3 fly-in.py