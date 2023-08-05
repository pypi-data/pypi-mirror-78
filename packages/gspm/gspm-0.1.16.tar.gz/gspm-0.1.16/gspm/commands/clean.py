
import logging
import argparse
import os


from argparse import ArgumentParser
import gspm.utils.godot_utils as godot_utils
import gspm.utils.asset_utils as asset_utils
import gspm.utils.path_utils as path_utils


def _run(project):

    # remove assets
    logging.log(99, "cleaning up project assets")
    if project.config.assets:
        for asset_name in project.config.assets:
            asset = project.config.assets[asset_name]
            asset.name = asset_name
            logging.info("- removing asset [{0}].".format(asset.name))
            if asset.active:
                asset_utils.clean_asset(project, asset)

    # remove project repo -- will leave behind residue
    logging.log(99, "cleaning up the repository")
    path_utils.clean_path(project.repository_path)

    # check if addons folder is empty and remove
    addons_path = os.path.abspath('{0}/addons'.format(project.home_path))
    logging.debug('- cleaning addons_path = {0}'.format(addons_path))
    if os.path.exists(addons_path):
        logging.info("- cleaning up addons folder")
        if not os.listdir(addons_path):
            path_utils.clean_path(addons_path)

    logging.log(99, "all done")


class Clean:

    @staticmethod
    def run(project):
        logging.debug("[Clean] run")
        _run(project)
        pass

    def add_parser(self, subparser: ArgumentParser):
        logging.debug("[Clean] add_parser")
        logging.debug("adding the [clean] command")

        cmd = subparser.add_parser("clean", help="remove all assets from the project")
        cmd.set_defaults(func=self.run)

        cmd.add_argument(
            "path",
            default=".",
            nargs="?",
            help="the path to the project",
        )

