"""matwrap.py: wrapper around matplotlib."""

import json
import logging
from argparse import _ArgumentGroup, Action, ArgumentParser
from contextlib import AbstractContextManager
from typing import Optional, Tuple, Union

from pkg_resources import resource_filename

from shinyutils import shiny_arg_parser
from shinyutils.argp import KeyValuePairsType

__all__ = ["MatWrap", "Plot"]


class MatWrap:

    _rc_defaults_path = resource_filename("shinyutils", "data/mplcfg.json")
    with open(_rc_defaults_path, "r") as f:
        _rc_defaults = json.load(f)

    _mpl = None
    _plt = None
    _sns = None

    @classmethod
    def configure(
        cls,
        context="paper",
        style="ticks",
        font="Latin Modern Roman",
        latex_pkgs=None,
        **rc_extra,
    ):
        """
        Arguments:
            context: seaborn context (paper/notebook/poster).
            style: seaborn style (whitegrid, darkgrid, etc.)
            font: latex font (passed directly to fontspec).
            latex_pkgs: list of packages to load in pgf preamble.
            rc_extra: matplotlib params (will overwrite defaults).
        """
        rc = MatWrap._rc_defaults.copy()
        rc["pgf.preamble"] = [r"\usepackage{fontspec}"]
        rc["pgf.preamble"].append(rf"\setmainfont{{{font}}}")
        rc["pgf.preamble"].append(rf"\setsansfont{{{font}}}")
        if latex_pkgs is not None:
            for pkg in reversed(latex_pkgs):
                rc["pgf.preamble"].insert(0, rf"\usepackage{{{pkg}}}")
        rc["pgf.preamble"] = "\n".join(rc["pgf.preamble"])
        rc.update(rc_extra)

        if cls._mpl is None:
            # pylint: disable=import-outside-toplevel
            try:
                import matplotlib
            except ImportError as e:
                e.msg += ": install shinyutils[plotting] to use MatWrap"
                raise e

            cls._mpl = matplotlib
            cls._mpl.rcParams.update(rc)

            import matplotlib.pyplot

            try:
                import seaborn
            except ImportError as e:
                e.msg += ": install shinyutils[plotting] to use MatWrap"
                raise e

            cls._plt = matplotlib.pyplot
            cls._sns = seaborn
        else:
            cls._mpl.rcParams.update(rc)
        cls._sns.set(context, style, rc=rc)

        cls._args = rc_extra.copy()
        cls._args["context"] = context
        cls._args["style"] = style
        cls._args["font"] = font
        cls._args["latex_pkgs"] = latex_pkgs

    def __new__(cls):
        raise NotImplementedError(
            "MatWrap does not provide instances. Use the class methods."
        )

    @classmethod
    def _ensure_conf(cls):
        if cls._mpl is None:
            cls.configure()

    @classmethod
    def mpl(cls):
        cls._ensure_conf()
        return cls._mpl

    @classmethod
    def plt(cls):
        cls._ensure_conf()
        return cls._plt

    @classmethod
    def sns(cls):
        cls._ensure_conf()
        return cls._sns

    @classmethod
    def palette(cls):
        return [
            "#e41a1c",
            "#6a3d9a",
            "#d55e00",
            "#34495e",
            "#377eb8",
            "#4daf4a",
            "#95a5a6",
            "#222222",
        ]

    @staticmethod
    def set_size_tight(fig, size):
        logging.warning(
            "constrained_layout is enabled by default: don't use tight_layout"
        )
        fig.set_size_inches(*size)
        fig.tight_layout(pad=0, w_pad=0, h_pad=0)

    @staticmethod
    def add_parser_config_args(
        base_parser: Union[ArgumentParser, _ArgumentGroup],
        group_title: Optional[str] = "plotting options",
    ) -> Union[ArgumentParser, _ArgumentGroup]:
        """Add arguments to a base parser to configure plotting."""

        class _ConfMatwrap(Action):
            def __call__(self, parser, namespace, values, option_string=None):
                _args = MatWrap._args
                assert option_string.startswith("--plotting-")
                option_name = option_string.split("--plotting-")[1].replace("-", "_")
                if option_name == "rc_extra":
                    MatWrap.configure(**_args, **values)
                else:
                    assert option_name in _args
                    _args[option_name] = values
                    MatWrap.configure(**_args)

        if group_title is not None:
            base_parser = base_parser.add_argument_group(group_title)

        base_parser.add_argument(
            "--plotting-context",
            type=str,
            choices=["paper", "notebook", "talk", "poster"],
            default="paper",
            action=_ConfMatwrap,
        )
        base_parser.add_argument(
            "--plotting-style",
            type=str,
            choices=["white", "dark", "whitegrid", "darkgrid", "ticks"],
            default="ticks",
            action=_ConfMatwrap,
        )
        base_parser.add_argument(
            "--plotting-font",
            type=str,
            default="Latin Modern Roman",
            action=_ConfMatwrap,
        )
        base_parser.add_argument(
            "--plotting-latex-pkgs",
            type=str,
            nargs="+",
            default=[],
            action=_ConfMatwrap,
        )
        base_parser.add_argument(
            "--plotting-rc-extra",
            type=KeyValuePairsType(),
            default=dict(),
            action=_ConfMatwrap,
        )

        return base_parser


class Plot(AbstractContextManager):
    """Wrapper around a single matplotlib plot."""

    def __init__(
        self,
        save_file: str,
        title: Optional[str] = None,
        sizexy: Optional[Tuple[int, int]] = None,
        labelxy: Tuple[Optional[str], Optional[str]] = (None, None),
        logxy: Tuple[bool, bool] = (False, False),
    ) -> None:
        self.save_file = save_file
        self.title = title
        self.sizexy = sizexy
        self.labelxy = labelxy

        self.fig = MatWrap.plt().figure()
        self.ax = self.fig.add_subplot(111)

        if logxy[0] is True:
            self.ax.set_xscale("log", nonposx="clip")
        if logxy[1] is True:
            self.ax.set_yscale("log", nonposy="clip")

    def __enter__(self):
        return self.ax

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            return

        if self.title is not None:
            self.ax.set_title(self.title)

        if self.labelxy[0] is not None:
            self.ax.set_xlabel(self.labelxy[0])
        if self.labelxy[1] is not None:
            self.ax.set_ylabel(self.labelxy[1])

        if self.sizexy is not None:
            self.fig.set_size_inches(*self.sizexy)

        self.fig.savefig(self.save_file)
        MatWrap.plt().close(self.fig)


MatWrap.configure()
MatWrap.add_parser_config_args(shiny_arg_parser)
