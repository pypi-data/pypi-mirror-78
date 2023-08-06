"""argp.py: utilities for argparse."""

import logging
import os
import re
import shutil
import sys
import textwrap
from argparse import ArgumentTypeError, FileType, HelpFormatter, SUPPRESS
from pathlib import Path
from typing import Any, Dict, Generic, IO, List, Optional, Type, TypeVar, Union
from unittest.mock import patch

from shinyutils.subcls import get_subclass_from_name, get_subclass_names

try:
    import crayons
except ImportError as e:
    CRAYONS_IMPORT_ERROR = e
    HAS_CRAYONS = False
else:
    HAS_CRAYONS = True


__all__ = [
    "LazyHelpFormatter",
    "comma_separated_ints",
    "CommaSeparatedInts",
    "InputFileType",
    "OutputFileType",
    "InputDirectoryType",
    "OutputDirectoryType",
    "ClassType",
    "KeyValuePairsType",
]


class LazyHelpFormatter(HelpFormatter):

    _CHOICE_SEP = "/"
    _UNICODE_REPL_SEP = "\ufffc"  # placeholder character for separator
    _CHOICES_START = "{"
    _CHOICES_END = "}"
    _UNICODE_REPL_START = "\ufffe"  # placeholder for choice list start
    _UNICODE_REPL_END = "\uffff"  # -"- end
    _LIST_SEP = ","
    _UNICODE_REPL_LISTSEP = "\ufffd"  # placeholder for list separator
    _PATTERN_HEXT = re.compile(r"\(.*?\)$", re.DOTALL)
    _PATTERN_DEFAULT = re.compile(r"(?<=default:).+(?=\))", re.DOTALL)
    _PATTERN_CHOICE = re.compile(
        fr"(?<=\({_CHOICES_START}|{_CHOICE_SEP} |  )"
        + fr"[^{_CHOICES_START}{_CHOICE_SEP}{_CHOICES_END}]+?"
        + fr"(?={_CHOICES_END}| (\n *)?{_CHOICE_SEP})"
    )

    use_colors: Optional[bool] = None
    _color_info_shown = False

    def _color_helper(self, s, color, isbold):
        try:
            s = s.group(0)
        except AttributeError:
            pass
        if not self._use_colors:
            return s
        color_fun = getattr(crayons, color)
        return str(color_fun(s, isbold))

    def _COLOR_KEYWORD(self, s):
        return self._color_helper(s, "green", isbold=False)

    def _COLOR_CHOICE(self, s):
        return self._color_helper(s, "blue", isbold=False)

    def _COLOR_DEFAULT(self, s):
        return self._color_helper(s, "yellow", isbold=True)

    def _COLOR_METAVAR(self, s):
        return self._color_helper(s, "red", isbold=True)

    @property
    def _DUMMY_CMV(self):
        # empty colored metavar
        return self._COLOR_METAVAR("")

    @property
    def _HELP_WIDTH(self):
        basew = shutil.get_terminal_size()[0]
        return basew + len(self._DUMMY_CMV)

    def _cstr(self, c):
        # pylint: disable=no-self-use
        # convert choice to string
        try:
            s = c.__name__
        except AttributeError:
            s = str(c)
        s = s.replace(self._CHOICES_START, self._UNICODE_REPL_START)
        s = s.replace(self._CHOICES_END, self._UNICODE_REPL_END)
        s = s.replace(self._CHOICE_SEP, self._UNICODE_REPL_SEP)
        s = s.replace(" ", "␣")
        s = s.replace("\n", "␤")
        s = s.replace("\r", "␍")
        return s

    def _dstr(self, d):
        # pylint: disable=no-self-use
        # convert default value to string
        if isinstance(d, (list, tuple)):
            slist = [self._dstr(di) for di in d]
            slist = [
                s.replace(self._LIST_SEP, self._UNICODE_REPL_LISTSEP) for s in slist
            ]
            return f"{self._LIST_SEP} ".join(slist)
        return self._cstr(d)

    def _format_action(self, action):
        if action.nargs == 0 and action.option_strings:
            # hack to fix length of option strings
            # when nargs=0, there's no metavar, or the extra color codes
            action.option_strings[0] += self._DUMMY_CMV

        # generate base format without help text
        help_ = action.help
        action.help = "\b"
        base_fmt = super()._format_action(action)

        # create formatted choice list
        if action.choices:
            choice_strs = f" {self._CHOICE_SEP} ".join(
                list(map(self._cstr, action.choices))
            )
            choice_list_fmt = (
                self._CHOICES_START + choice_strs + self._CHOICES_END + " "
            )
        else:
            choice_list_fmt = ""

        # compute extra help text (required/optional/default)
        if not action.option_strings:
            # positional arguments can't be optional, don't have defaults,
            #   and are always required - so no extra text required
            hext = f"({choice_list_fmt[:-1]})" if choice_list_fmt else None
        elif action.required:
            # indicate optional arguments which are required
            hext = f"({choice_list_fmt}required)"
        elif action.default is None or action.default == SUPPRESS:
            hext = f"({choice_list_fmt}optional)"
        else:
            hext = f"({choice_list_fmt}default: {self._dstr(action.default)})"

        # combine 'base_fmt' with 'help_' and 'hext'
        fmt = base_fmt.strip("\n")
        if help_:
            fmt += " " + help_
        if hext:
            fmt += (" " if help_ or action.nargs != 0 else "") + hext

        # wrap the formatted text
        # indentation computation needs to take color codes into account
        #   and i'm not completely certain why this is correct
        indent = self._COLOR_METAVAR("\b\b") + " " * (
            len(base_fmt.strip("\n"))
            - len(self._DUMMY_CMV)
            - 1
            + self._indent_increment
        )
        fmt = textwrap.fill(
            fmt,
            width=self._HELP_WIDTH,
            subsequent_indent=indent,
            break_on_hyphens=False,
            break_long_words=True,
        )

        # add colors to 'hext' inside the formatted text
        fmt_hext_match = re.search(self._PATTERN_HEXT, fmt)
        if fmt_hext_match:
            fmt_hext = fmt_hext_match.group(0)
            # color default values
            def_match = re.search(self._PATTERN_DEFAULT, fmt_hext)
            if def_match:
                def_match = def_match.group(0)
                def_match_colored = def_match.replace(self._COLOR_METAVAR("\b\b"), "")
                if isinstance(action.default, (list, tuple)):
                    # color individual items in the sequence then join
                    def_match_pieces = def_match_colored.split(f"{self._LIST_SEP}")
                    if def_match_pieces[0].startswith(" "):
                        def_match_pieces[0] = def_match_pieces[0][1:]
                    def_match_pieces_colored = list(
                        map(self._COLOR_DEFAULT, def_match_pieces)
                    )
                    def_match_colored = f"{self._LIST_SEP}".join(
                        def_match_pieces_colored
                    )
                    def_match_colored = def_match_colored.replace(
                        self._UNICODE_REPL_LISTSEP, self._LIST_SEP
                    )
                    if isinstance(action.default, list):
                        def_match_colored = " [" + def_match_colored + "]"
                    else:
                        def_match_colored = " (" + def_match_colored + ")"
                else:
                    def_match_colored = self._COLOR_DEFAULT(def_match_colored)
                fmt_hext_colored = re.sub(
                    self._PATTERN_DEFAULT, def_match_colored, fmt_hext
                )
                fmt_hext_colored = re.sub(
                    "default", self._COLOR_KEYWORD, fmt_hext_colored, count=1
                )
            else:
                fmt_hext_colored = fmt_hext

            # color keywords
            if action.required:
                fmt_hext_colored = self._COLOR_KEYWORD("required").join(
                    fmt_hext_colored.rsplit("required", 1)
                )
            elif action.default is None or action.default == SUPPRESS:
                fmt_hext_colored = self._COLOR_KEYWORD("optional").join(
                    fmt_hext_colored.rsplit("optional", 1)
                )

            # color choices
            fmt_hext_colored = re.sub(
                self._PATTERN_CHOICE, self._COLOR_CHOICE, fmt_hext_colored
            )

            # replace the placeholders with separators
            fmt_hext_colored = fmt_hext_colored.replace(
                self._UNICODE_REPL_SEP, self._CHOICE_SEP
            )
            fmt_hext_colored = fmt_hext_colored.replace(
                self._UNICODE_REPL_START, self._CHOICES_START
            )
            fmt_hext_colored = fmt_hext_colored.replace(
                self._UNICODE_REPL_END, self._CHOICES_END
            )

            # replace hext in the formatted text with the new colored version
            fmt = fmt.replace(fmt_hext, fmt_hext_colored)

        return fmt + "\n"

    def _format_action_invocation(self, action):
        if action.option_strings and action.nargs != 0:
            # show action as -s/--long ARGS rather than -s ARGS, --long ARGS
            combined_opt_strings = self._CHOICE_SEP.join(action.option_strings)
            with patch.object(action, "option_strings", [combined_opt_strings]):
                return super()._format_action_invocation(action)

        with patch.object(  # format positional arguments same as optional
            action, "option_strings", action.option_strings or [action.dest]
        ):
            return super()._format_action_invocation(action)

    def _get_default_metavar_for_optional(self, action):
        if action.type:
            try:
                return action.type.metavar
            except AttributeError:
                try:
                    return action.type.__name__
                except AttributeError:
                    return type(action.type).__name__
        return None

    def _get_default_metavar_for_positional(self, action):
        if action.type:
            try:
                return action.type.metavar
            except AttributeError:
                try:
                    return action.type.__name__
                except AttributeError:
                    return type(action.type).__name__
        return None

    def _metavar_formatter(self, action, default_metavar):
        with patch.object(action, "choices", None):
            # don't put choices in the metavar
            base_formatter = super()._metavar_formatter(action, default_metavar)

        def color_wrapper(tuple_size):
            f = base_formatter(tuple_size)
            if not f:
                return f
            return (
                self._COLOR_METAVAR(" ".join(map(str, f))),
                *(("",) * (len(f) - 1)),  # collapse to single metavar
            )

        return color_wrapper

    def __init__(self, prog: str, indent_increment: int = 2) -> None:
        cls = self.__class__
        self._use_colors: bool
        if cls.use_colors is False:
            self._use_colors = False
        elif cls.use_colors is True:
            self._use_colors = True
            if not HAS_CRAYONS:
                raise ImportError(
                    f"{CRAYONS_IMPORT_ERROR}: "
                    "disable colors or install shinyutils[color]"
                )
        else:
            self._use_colors = HAS_CRAYONS
            if not HAS_CRAYONS and not cls._color_info_shown:
                logging.info("for argparse color support install shinyutils[color]")
                cls._color_info_shown = True

        max_help_position = sys.maxsize
        width = sys.maxsize
        super().__init__(prog, indent_increment, max_help_position, width)

    def add_usage(self, *args: Any, **kwargs: Any) -> None:
        # pylint: disable=signature-differs
        pass

    def start_section(self, heading: Optional[str] = None) -> None:
        if heading == "positional arguments":
            heading = "arguments"
        elif heading == "optional arguments":
            heading = "options"
        super().start_section(heading)


def comma_separated_ints(string: str) -> List[int]:
    logging.warning("comma_separated_ints is deprecated and will be removed")
    try:
        return list(map(int, string.split(",")))
    except:
        raise ArgumentTypeError(
            f"`{string}` is not a comma separated list of ints"
        ) from None


class CommaSeparatedInts:

    metavar = "int,[...]"

    def __call__(self, string: str) -> List[int]:
        try:
            return list(map(int, string.split(",")))
        except:
            raise ArgumentTypeError(
                f"`{string}` is not a comma separated list of ints"
            ) from None


class InputFileType(FileType):

    metavar = "file"

    def __init__(
        self,
        mode: str = "r",
        bufsize: int = -1,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
    ) -> None:
        if mode not in {"r", "rb"}:
            raise ValueError("mode should be 'r'/'rb'")
        super().__init__(mode, bufsize, encoding, errors)

    def __call__(self, string: str) -> IO:
        # pylint: disable=useless-super-delegation
        return super().__call__(string)


class OutputFileType(FileType):

    metavar = "file"

    def __init__(
        self,
        mode: str = "w",
        bufsize: int = -1,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
    ) -> None:
        if mode not in {"w", "wb"}:
            raise ValueError("mode should be 'w'/'wb'")
        super().__init__(mode, bufsize, encoding, errors)

    def __call__(self, string: str) -> IO:
        file_dir = os.path.dirname(string)
        if file_dir and not os.path.exists(file_dir):
            logging.warning(f"no directory for {string}: trying to create")
            try:
                os.makedirs(file_dir)
            except Exception as e:
                raise ArgumentTypeError(f"could not create {file_dir}") from e
            logging.info(f"created {file_dir}")
        return super().__call__(string)


class InputDirectoryType:

    metavar = "dir"

    def __call__(self, string: str) -> Path:
        if not os.path.exists(string):
            raise ArgumentTypeError(f"no such directory: {string}")
        if not os.path.isdir(string):
            raise ArgumentTypeError(f"{string} is a file: expected directory")
        return Path(string)


class OutputDirectoryType:

    metavar = "dir"

    def __call__(self, string: str) -> Path:
        if not os.path.exists(string):
            logging.warning(f"{string} not found: trying to create")
            try:
                os.makedirs(string)
            except Exception as e:
                raise ArgumentTypeError(f"cound not create {string}") from e
            logging.info(f"created {string}")
        elif not os.path.isdir(string):
            raise ArgumentTypeError(f"{string} is a file: expected directory")
        return Path(string)


T = TypeVar("T")


class ClassType(Generic[T]):

    metavar = "cls"

    def __init__(self, cls: Type[T]) -> None:
        self.cls = cls

    def __call__(self, string: str) -> Type[T]:
        try:
            return get_subclass_from_name(self.cls, string)
        except RuntimeError:
            choices = [f"'{c}'" for c in get_subclass_names(self.cls)]
            raise ArgumentTypeError(
                f"invalid choice: '{string}' " f"(choose from {', '.join(choices)})"
            ) from None


class KeyValuePairsType:

    metavar = "str=val[,...]"
    ValType = Union[int, float, str]

    def __call__(self, string: str) -> Dict[str, ValType]:
        out = dict()
        try:
            for kv in string.split(","):
                k, v = kv.split("=")
                pv: KeyValuePairsType.ValType = v
                try:
                    pv = int(v)
                except ValueError:
                    try:
                        pv = float(v)
                    except ValueError:
                        pass
                out[k] = pv
        except Exception as e:
            raise ArgumentTypeError() from e
        return out
