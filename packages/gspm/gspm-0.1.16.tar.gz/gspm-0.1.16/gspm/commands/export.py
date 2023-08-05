
import logging
import argparse
import os


from argparse import ArgumentParser
import gspm.utils.godot_utils as godot_utils
import gspm.utils.asset_utils as asset_utils
import gspm.utils.path_utils as path_utils


def _run(project):

    logging.debug("[export] _run")

    if project.args.name not in project.config.exports:
        raise Exception("Could Not Find The Export [{0}] In Your Configuration File".format(project.args.name))

    export = project.config.exports[project.args.name]

    # use export name if not specified on export config
    if not export.name:
        export.name = project.args.name 

    # check that folder exists
    if not os.path.exists(export.path):
        os.makedirs(export.path)

    path = "{0}/{1}".format(export.path, export.file)
    err = godot_utils.export_godot(project, export.name, path)
    print(err)
    logging.log(99, "project {0} has been exported".format(project.config.name))


class Export:

    @staticmethod
    def run(project):
        logging.debug("[export] run")
        _run(project)
        pass

    def add_parser(self, subparser: ArgumentParser):
        logging.debug("- adding the [export] command")

        cmd = subparser.add_parser("export", help="export your game")
        cmd.set_defaults(func=self.run)

        cmd.add_argument(
            "name",
            default=".",
            nargs="?",
            help="the name of the export",
        )


