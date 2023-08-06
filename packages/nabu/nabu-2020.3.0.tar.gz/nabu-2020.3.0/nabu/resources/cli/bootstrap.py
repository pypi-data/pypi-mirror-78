from os import path
from .utils import parse_params_values
from .cli_configs import BootstrapConfig
from ...io.config import generate_nabu_configfile
from ..validators import convert_to_bool

def parse_sections(sections):
    sections = sections.lower()
    if sections == "all":
        return None
    sections = sections.replace(" ", "").split(",")
    return sections



def bootstrap():
    args = parse_params_values(
        BootstrapConfig,
        parser_description="Initialize a nabu configuration file"
    )

    do_bootstrap = bool(args["bootstrap"])
    do_convert = (args["convert"] != "")
    no_comments = bool(args["nocomments"])

    if (do_bootstrap ^ do_convert) == 0:
        print("You must specify either --bootstrap or --convert")
        exit(0)

    if path.isfile(args["output"]):
        rep = input("File %s already exists. Overwrite ? [y/N]" % args["output"])
        if rep.lower() != "y":
            print("Stopping")
            exit(0)

    if do_bootstrap:
        generate_nabu_configfile(
            args["output"],
            comments=not(no_comments),
            options_level=args["level"],
        )
    else: # do_convert
        print("PyHST file converter is not implemented yet")
        exit(1)

