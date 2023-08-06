"""test_argp_formatter.py: script with various argument types to check formatting."""

from shinyutils import shiny_arg_parser

shiny_arg_parser.add_argument("arg", type=str, metavar="ARG", help="standard argument")
shiny_arg_parser.add_argument("arg_no_help_meta", type=str)
shiny_arg_parser.add_argument("arg_n2", type=int, nargs=2, help="argument with nargs>1")
shiny_arg_parser.add_argument(
    "arg_choices_no_help", type=int, metavar="ARG", choices=[1, 2, 3]
)
shiny_arg_parser.add_argument(
    "arg_choices_n2",
    type=str,
    nargs=2,
    choices=["3.14", "2.71"],
    help="choices for nargs>1",
)

shiny_arg_parser.add_argument(
    "-o", "--opt", type=float, help="standard option", default=3.14
)
shiny_arg_parser.add_argument(
    "--opt-many-choices", type=int, choices=range(100, 201), default=123
)
shiny_arg_parser.add_argument(
    "--opt-choices-no-default", type=int, choices=[1, 10, 100], help="no default value"
)
shiny_arg_parser.add_argument("-O", type=str, help="only short option")
shiny_arg_parser.add_argument(
    "--opt-req", type=float, nargs=3, required=True, help="this is required"
)
shiny_arg_parser.add_argument("--do-it", action="store_true", help="store true option")
shiny_arg_parser.add_argument(
    "--dont-do-it", action="store_false", help="store false option"
)
shiny_arg_parser.add_argument("--r", metavar="are", help="custom metavar")

grp = shiny_arg_parser.add_argument_group("group")
grp.add_argument(
    "--g1", type=int, default=0, choices=[1, 2, 3], help="default not in choices"
)
grp.add_argument("--g2", type=str, default="hello, world")

shiny_arg_parser.add_argument(
    "--optopt", type=float, nargs="?", help="optional through nargs"
)
shiny_arg_parser.add_argument(
    "--opt-many", nargs="+", help="option with multiple values"
)
shiny_arg_parser.add_argument(
    "--bad-choices",
    type=str,
    choices=[
        "a/b",
        "a / b",
        " [ ] ",
        " ( ) ",
        "[hello]",
        "{}",
        "{0",
        "0}",
        "(}",
        "{]",
        "{{)(}}]][[",
        '"',
        "a b",
        "  ",
        "'ab'",
        "a,b",
        "str",
        "int",
        "default",
        "optional",
        "required",
    ],
)
shiny_arg_parser.add_argument("--long-help", type=int, help="help " * 25)
shiny_arg_parser.add_argument("--long-help-single-word", type=int, help="help" * 25)

shiny_arg_parser.add_argument(
    "--keywords-in-default", type=str, default="str int default optional required"
)
shiny_arg_parser.add_argument("--newline-in-default", type=str, default="a\nb")
shiny_arg_parser.add_argument(
    "--list-default", type=str, nargs="*", default=["a", "b", "c"]
)
shiny_arg_parser.add_argument(
    "--tuple-default", type=str, nargs="*", default=("a", "b", "c")
)
shiny_arg_parser.add_argument(
    "--bad-list-default",
    type=str,
    nargs="*",
    default=[
        "a/b",
        "a / b",
        " [ ] ",
        " ( ) ",
        "[hello]",
        "{}",
        "{0",
        "0}",
        "(}",
        "{]",
        "{{)(}}]][[",
        '"',
        "a b",
        "  ",
        "'ab'",
        "a,b",
        "str",
        "int",
        "default",
        "optional",
        "required",
    ],
)
shiny_arg_parser.add_argument(
    "--long-default",
    type=str,
    default=(" default " * 10 + "\n" + "default" * 10 + "\n" + "default " * 10),
)

shiny_arg_parser.print_help()
