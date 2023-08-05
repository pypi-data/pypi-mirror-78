
import argparse
import gspm

from gspm.commands.new import New
from gspm.commands.install import Install
from gspm.commands.edit import Edit
from gspm.commands.run import Run
from gspm.commands.update import Update
from gspm.commands.clean import Clean
from gspm.commands.test import Test
from gspm.commands.export import Export


def _create_options(parser):

    parser.add_argument(
        "-f",
        "--force",
        dest="force",
        action="store_true",
        help="force a command to execute with warnings",
        default=False
    )

    parser.add_argument(
        "-c",
        "--config",
        dest="config",
        help="use a different configuration file",
        default="project.yml"
    )

    parser.add_argument(
        "--quiet",
        dest="quiet",
        action="store_true",
        help="show less information when running",
        default=False
    )

    parser.add_argument(
        "--verbose",
        dest="verbose",
        action="store_true",
        help="show more information when running",
        default=False
    )

    parser.add_argument(
        "--more-verbose",
        dest="more_verbose",
        action="store_true",
        help="show all information when running",
        default=False
    )

    parser.add_argument(
        "--version",
        action="version",
        version="",
        help="show version"
    )

    parser.add_argument(
        "--ignore-project",
        dest="ignore_project",
        action="store_true",
        help=argparse.SUPPRESS,
        default=False
    )

    parser.add_argument(
        "--log",
        dest="log",
        action="store_true",
        help="log everything to gspm.log file",
        default=False
    )


def _create_commands(subparser):

    edit = Edit()
    edit.add_parser(subparser)

    install = Install()
    install.add_parser(subparser)

    update = Update()
    update.add_parser(subparser)

    new = New()
    new.add_parser(subparser)

    run = Run()
    run.add_parser(subparser)

    clean = Clean()
    clean.add_parser(subparser)

    test = Test()
    test.add_parser(subparser)

    export = Export()
    export.add_parser(subparser)


def create_parser():

    parser = argparse.ArgumentParser(prog='gspm', description=gspm.__desc__)
    subparser = parser.add_subparsers(dest='command')
    subparser.required = True

    _create_options(parser)
    _create_commands(subparser)

    return parser
