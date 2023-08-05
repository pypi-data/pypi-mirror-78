# ============= ANSI ==============
import pydoc
import shutil
from typing import Callable

ANSI_RESET = "\033[0m"
ANSI_BOLD = "\033[1m"
ANSI_UNDERLINE = "\033[4m"

# ========= HMD CONSTANTS ==========

A_NONE = -1

F_NONE = 0
F_BOLD = 1
F_ITALIC = 2

STATE_NONE = 0
STATE_FMT = 1
STATE_FMT_2 = 2

MARK_FMT = "*"
MARK_ESCAPE = "\\"

DIRECTIVE_PREFIX = "."
DIRECTIVE_A_BEGIN = f"{DIRECTIVE_PREFIX}A"
DIRECTIVE_A_NEEDLE = "."
DIRECTIVE_A_END = f"{DIRECTIVE_PREFIX}/A"

# ============== UTILS ==============

verbose = False

def _vprint(*args, **kwargs):
    if not verbose:
        return
    print(*args, **kwargs)


def _termsize(fallback=(80, 24)):
    """ Returns the terminal size, or the fallback if it can't be retrieved"""
    try:
        columns, rows = shutil.get_terminal_size(fallback=fallback)
    except:
        return fallback
    return columns, rows


# ========== HMD FILTERS =============

class HMDFilter:
    """ Encapsulates formatting tags. """
    def __init__(self):
        self.bold_begin = ""
        self.bold_end = ""
        self.italic_begin = ""
        self.italic_end = ""


def ansi_filter() -> HMDFilter:
    hmd_filter = HMDFilter()
    hmd_filter.bold_begin = ANSI_BOLD
    hmd_filter.bold_end = ANSI_RESET
    hmd_filter.italic_begin = ANSI_UNDERLINE
    hmd_filter.italic_end = ANSI_RESET
    return hmd_filter


def text_filter() -> HMDFilter:
    hmd_filter = HMDFilter()
    return hmd_filter


# =============== HMD ==================

class HMD:
    """
    Processor of .hmd documents.
    Read .hmd files and gives a formatted output.
    """

    def __init__(self,
                 columns=None,
                 hmd_filter: Callable=ansi_filter):
        self._columns = columns or _termsize()[0]
        self._filter = hmd_filter()
        self._out = ""

        self._state = STATE_NONE
        self._escaping = False
        self._format = F_NONE
        self._align = A_NONE

        self._just_space = False
        self._just_break = False

        self._line = None
        self._indent = 0
        self._row = 0
        self._col = 0

    def _reset(self):
        self._out = ""

        self._state = STATE_NONE
        self._escaping = False
        self._format = F_NONE
        self._align = A_NONE

        self._just_space = False
        self._just_break = False

        self._line = None
        self._indent = 0
        self._row = 0
        self._col = 0


    def render(self, content: str):
        """
        Renders the output of convert() using the default pager (typically less).
        :param content: the document content
        """
        pydoc.pager(self.convert(content))


    def convert(self, content: str):
        """
        Reads the content of a .hmd `document` and returns the formatted output.
        :param content: the document content
        :return: the processed and formatted content
        """

        self._reset()

        def indent_of_line(l):
            """
            Returns the count of leading whitespaces of the given line
            :param l: a line
            :return: the # of leading whitespaces
            """
            ind = 0
            for ch in l:
                if ch == " ":
                    ind += 1
                else:
                    break
            return ind

        # Split by lines, joining those if are ending with \
        lines = []
        original_lines = content.splitlines()
        extended_line = ""

        indent = None
        for line in original_lines:
            if indent is None:
                # Compute the indention of the line
                indent = indent_of_line(line)

            if line.endswith("\\"):
                join = True
                line = line[:len(line) - 1]
            else:
                join = False

            # Keep only the part after the indentation
            extended_line += line[indent:]

            if join:
                continue

            lines.append((extended_line, indent))
            extended_line = ""
            indent = None

        for line_idx, (line, indent) in enumerate(lines):
            _vprint(f"{line_idx}) {indent}-> : {line}")

            self._col = 0
            self._indent = indent
            self._line = line

            # Directive (starting with .)
            if line.startswith(DIRECTIVE_PREFIX):
                self._handle_directive(line, indent)
                continue

            # Normal characters
            i = 0
            while i < len(self._line):
                c = self._line[i]
                next_c = self._line[i + 1] if i < len(self._line) - 1 else '\0'
                skip_next = self._handle_char(c, next_c)
                i += 1 + skip_next

            # \n
            self._handle_eol()

        if not self._out:
            return ""

        # Strip the last \n
        return self._out[:len(self._out) - 1]

    def _handle_directive(self, line: str, indent: int):
        """
        Handles directives (starting with .).
        :param line: the line for which handle the directive
        """
        if line.startswith(DIRECTIVE_A_BEGIN):
            # Align Begin
            self._align = indent + line.rfind(DIRECTIVE_A_NEEDLE)
        elif line.startswith(DIRECTIVE_A_END):
            # Align End
            self._align = A_NONE

        # Everything else starting with '.' is a comment

    def _handle_char(self, char: str, next_char: str):
        """
        Handles a character.
        :param char: the character to handle
        :param next_char: the character after the one to handle, or None if it
                        is the last
        :return: the number of next characters to skip (usually is 0)
        """
        _vprint(f"({self._row}, {self._col}) [I={self._indent}] = {char}")

        skip_next = 0

        if self._escaping:
            # Was escaping due to a \, treat everything as literal
            _vprint("ESCAPE off")
            self._escaping = False
        else:
            # Not escaping

            # '*' : format mark for bold/italic
            if char == MARK_FMT:
                if self._state == STATE_FMT_2:
                    # Apply it now
                    self._apply_format()

                if self._state == STATE_NONE:
                    self._state = STATE_FMT
                elif self._state == STATE_FMT:
                    self._state = STATE_FMT_2
                return skip_next
            # '\' : escape next char
            if char == MARK_ESCAPE:
                _vprint("ESCAPE on")
                self._escaping = True
                return skip_next


        if self._col == 0:
            # Apply indent for the first char of the line
            self._out += " " * self._indent
        else:
            # Line break handling (based on `columns`)

            q1, r1 = divmod(self._col,
                            (self._columns - self._indent - 1))

            if self._align == A_NONE:
                # Normal case: break if we reached the end of the line
                br = r1 == 0
            else:
                # Align override case: break if we reached the end of the line,
                # taking into account if we are on the first or on the further lines
                q2, r2 = divmod((self._col - (self._columns - self._indent - 1)),
                                (self._columns - self._align - 1))

                br = (q1 == 1 and r1 == 0) or (q2 > 0 and r2 == 0)

            if br:
                # Disable formatting before break line and enable it again
                # after the line break
                was_bold = self._format == F_BOLD
                was_italic = self._format == F_ITALIC
                if was_bold:
                    self._b()
                if was_italic:
                    self._i()

                # Add a '-', but only if the new char is a non white space and
                # the last was a space
                if char != " " and not self._just_space:
                    if next_char != " ":
                        # Add a - since what follows is text
                        self._out += "-"
                    else:
                        # Follows a space, render the last char instead of -
                        # but skip it
                        _vprint(f"BREAKING WITH {char} - skip next")
                        self._out += char
                        skip_next = 1

                # Actually break with new line
                self._out += "\n"
                self._just_break = True

                if self._align != A_NONE and self._col != 0:
                    # Align override case: indent by `align` amount
                    self._out += " " * self._align
                else:
                    # Normal case: indent by `indent` amount
                    self._out += " " * self._indent

                # Restore formatting
                if was_bold:
                    self._b()
                if was_italic:
                    self._i()

        if not skip_next:
            if char == " " and self._just_break:
                # Space on a new line after break, avoid render it (for keep the
                # first character aligned with the right indentation)
                pass
            else:
                # Normal case: add the character to the output,
                # eventually applying formatting
                self._apply_format()
                self._just_space = char == " "
                self._out += char

        self._col += 1 + skip_next
        self._just_break = False

        return skip_next

    def _handle_eol(self):
        """
        Handles end of current line, adding \n and performing
        other stuff such as applying formatting.
        """
        # Eventually apply format request right now, before new line
        self._apply_format()
        self._out += "\n"
        self._row += 1

    def _apply_format(self):
        """ Apply the format (bold or italic) if needed. """
        if self._state == STATE_FMT_2:
            self._b()
        elif self._state == STATE_FMT:
            self._i()
        self._state = STATE_NONE

    def _b(self):
        """ Opens or close a bold format, depending on the current format state """
        if self._format == F_NONE:
            self._out += self._filter.bold_begin
            self._format = F_BOLD
            _vprint("BOLD on")
        elif self._format == F_BOLD:
            self._out += self._filter.bold_end
            self._format = F_NONE
            _vprint("BOLD off")

    def _i(self):
        """ Opens or close an italic format, depending on the current format state """
        if self._format == F_NONE:
            self._out += self._filter.italic_begin
            self._format = F_ITALIC
            _vprint("ITALIC on")
        elif self._format == F_ITALIC:
            self._out += self._filter.italic_end
            self._format = F_NONE
            _vprint("ITALIC off")