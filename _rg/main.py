import os
from argparse import ArgumentParser

from _rg.classes.RenderSettings import RenderSettings, RenderMode
from _rg.classes.renderables.Resume import Resume
from _rg.classes.renderables.potential_content.PotentialContent import PotentialContent
from definitions import ROOT_DIR

PROD_OUTPUT_DIRECTORY = os.path.join(ROOT_DIR, "../output")
DEV_OUTPUT_DIRECTORY = os.path.join(ROOT_DIR, "out")


def generate_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("-d", "--dev-output",
                        help=f"Outputs into the test output directory({DEV_OUTPUT_DIRECTORY}) "
                             f"rather than the default({PROD_OUTPUT_DIRECTORY})",
                        action="store_const", const=DEV_OUTPUT_DIRECTORY)
    parser.add_argument("-o", "--output-mode",
                        choices=[x.name.lower() for x in RenderMode],
                        default=RenderMode.PARSABLE)
    return parser


def process_args(args):
    output_directory = args.dev_output
    if output_directory is None:
        output_directory = PROD_OUTPUT_DIRECTORY

    PotentialContent.dump_all_schemas()

    Resume().generate_file(output_directory, RenderSettings())


def run_cli():
    parser = generate_parser()
    args = parser.parse_args()

    process_args(args)


if __name__ == '__main__':
    run_cli()
