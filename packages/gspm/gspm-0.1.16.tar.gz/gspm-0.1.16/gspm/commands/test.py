
import logging
import argparse
import os


from argparse import ArgumentParser
import gspm.utils.godot_utils as godot_utils
import gspm.utils.asset_utils as asset_utils
import gspm.utils.path_utils as path_utils


def _run(project):
    exit = godot_utils.run_godot_script(project, "addons/WAT/cli.tscn -run_dir=res://tests")
    print(exit)


class Test:

    @staticmethod
    def run(project):
        logging.debug("[Test] run")
        _run(project)
        pass

    def add_parser(self, subparser: ArgumentParser):
        logging.debug("[Test] add_parser")
        logging.debug("adding the [test] command")

        cmd = subparser.add_parser("test", help="run unit tests in your project")
        cmd.set_defaults(func=self.run)

        cmd.add_argument(
            "path",
            default=".",
            nargs="?",
            help="the path to the project",
        )

