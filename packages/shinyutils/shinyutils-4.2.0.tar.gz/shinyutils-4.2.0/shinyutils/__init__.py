__version__ = "4.2.0"

import argparse as _argparse

from shinyutils.argp import *
from shinyutils.logng import *

conf_logging()
shiny_arg_parser = _argparse.ArgumentParser(formatter_class=LazyHelpFormatter)
build_log_argp(shiny_arg_parser)
