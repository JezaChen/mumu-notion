""" Collection of print tools with styles """
from enum import Enum

__all__ = [
    "PrintStyle",
    "colored_print",
    "generate_step_printer",
    "press_enter_to_continue"
]


class PrintStyle(Enum):
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    DEFAULT = ''


def colored_print(value: str,
                  color: PrintStyle = PrintStyle.DEFAULT,
                  *args,
                  **kwargs):
    print(f"{color.value}{value}\033[0m", *args, **kwargs)


def generate_step_printer(color: PrintStyle = PrintStyle.YELLOW):
    step_counter = 0

    def _print_step(value: str, *args, **kwargs):
        nonlocal step_counter
        step_counter += 1
        colored_print(f"\nStep {step_counter}: " + value,
                      color=color,
                      *args,
                      **kwargs)

    return _print_step


def press_enter_to_continue():
    colored_print("Press ENTER to go to the next step...",
                  color=PrintStyle.GREEN,
                  end="")
    input()
