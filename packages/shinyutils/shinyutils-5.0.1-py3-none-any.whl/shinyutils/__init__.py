import argparse as _argparse

from shinyutils._version import __version__
from shinyutils.argp import *
from shinyutils.logng import *

conf_logging()
shiny_arg_parser = _argparse.ArgumentParser(formatter_class=LazyHelpFormatter)
build_log_argp(shiny_arg_parser)
