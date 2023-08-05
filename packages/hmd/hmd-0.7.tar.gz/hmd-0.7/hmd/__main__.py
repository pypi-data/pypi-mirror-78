import argparse
import sys
from pathlib import Path

from hmd.hmd import HMD, text_filter, ansi_filter

""" AUTOMATICALLY GENERATED 
usage: __main__.py [-h] [-t] [-n] [-c COLUMNS] [input]

Render documents written in hmd (Help MarkDown) with the default pager. Reads from 'input' or from stdin if it is not given.

positional arguments:
  input                 Help MarkDown file to process and render

optional arguments:
  -h, --help            show this help message and exit
  -t, --text            Output text, without ANSI style
  -n, --no-pager        Just print, without using the pager
  -c COLUMNS, --columns COLUMNS
                        Override columns number (by default it depends on the terminal size)
"""


def main():
    parser = argparse.ArgumentParser(
        description="""\
Render documents written in hmd (Help MarkDown) with the default pager.
Reads from 'input' or from stdin if it is not given.
"""
    )

    # --text
    parser.add_argument("-t", "--text",
                        action="store_const", const=True, default=False,
                        dest="text",
                        help="Output text, without ANSI style")

    # --no-pager
    parser.add_argument("-n", "--no-pager",
                        action="store_const", const=True, default=False,
                        dest="no_pager",
                        help="Just print, without using the pager")

    # --columns <col>
    parser.add_argument("-c", "--columns",
                        dest="columns", metavar="COLUMNS", type=int,
                        help="Override columns number (by default it depends on the terminal size)")

    # positional argument (document)
    parser.add_argument("input",
                        nargs="?",
                        help="Help MarkDown file to process and render")


    parsed = vars(parser.parse_args(sys.argv[1:]))
    text_only = parsed.get("text")
    columns = parsed.get("columns")
    no_pager = parsed.get("no_pager")

    hmd_content = None

    if parsed.get("input"):
        # Read from given file
        hmd_input = Path(parsed["input"]).expanduser()

        if not hmd_input.exists():
            print(f"Not exists: '{hmd_input}'")
            exit(-1)

            try:
                hmd_content = hmd_input.open().read()
            except:
                print(f"Cannot read '{hmd_input}'")
                exit(-1)
    else:
        # Read from stdin
        hmd_content = sys.stdin.read()

    hmd = HMD(columns=columns,
              hmd_filter=text_filter if text_only else ansi_filter)

    if no_pager:
        print(hmd.convert(hmd_content))
    else:
        hmd.render(hmd_content)

if __name__ == '__main__':
    main()