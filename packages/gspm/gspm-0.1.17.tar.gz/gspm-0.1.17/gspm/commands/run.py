
import logging
import argparse

from argparse import ArgumentParser
import gspm.utils.godot_utils as godot_utils


def _run(project):
    godot_utils.run_godot(project)


class Run:

    @staticmethod
    def run(project):
        logging.debug("[Run] run")
        _run(project)
        pass

    def add_parser(self, subparser: ArgumentParser):
        logging.debug("[Run] add_parser")
        logging.debug("adding [run] command")

        cmd = subparser.add_parser("run", help="run the project")
        cmd.set_defaults(func=self.run)
        
        cmd.add_argument(
            "path",
            default=".",
            nargs="?",
            help="the path to the project",
        )
        

