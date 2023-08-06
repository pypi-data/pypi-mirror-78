"""
Functions for generating code badges
"""

__all__ = [
    "print_pylint_badge",
]

from collections import OrderedDict
from contextlib import redirect_stdout
import sys


def print_pylint_badge():
    "Runs the pylint executable and prints the badge with the score"
    from pylint.lint import Run

    with redirect_stdout(sys.stderr):
        results = Run(sys.argv[1:], do_exit=False)

    score = results.linter.stats["global_note"]
    colors = OrderedDict(
        {
            9.95: "brightgreen",
            8.95: "green",
            7.95: "yellowgreen",
            6.95: "yellow",
            5.95: "orange",
            0.00: "red",
        }
    )

    for val, color in colors.items():
        if score >= val:
            break

    print(
        "[![pylint](https://img.shields.io/badge/pylint%%20score-%.1f%%2F10-%s?logo=python&logoColor=white)](http://pylint.pycqa.org/)"
        % (score, color)
    )
