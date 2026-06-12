import os
import sys
from source import Controller
from colorama import Fore, Style


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
        print("Bye Bye")


if __name__ == "__main__":
    main()
