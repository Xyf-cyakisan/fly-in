import os
import sys
from source import Controller
try:
    from colorama import Fore, Style
except ImportError:
    print(
        "\033[0;31mError: 'Colorama' module not found,"
        "please run 'make install' command before 'make run'\033[0m"
    )
    sys.exit(4)


def main() -> None:
    try:
        print("\033c", end="")
        controller = Controller(os.getenv("MAP"))
        controller.run()
    except ValueError as value_error:
        print(f"{Fore.RED}{value_error}{Style.RESET_ALL}")
        sys.exit(1)
    except FileNotFoundError as file_error:
        print(f"{Fore.RED}{file_error}{Style.RESET_ALL}")
        sys.exit(2)
    except PermissionError as perm_error:
        print(f"{Fore.RED}{perm_error}{Style.RESET_ALL}")
        sys.exit(3)
    except KeyboardInterrupt:
        print("\033c")
        print(f"{Fore.BLUE}Bye Bye{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
