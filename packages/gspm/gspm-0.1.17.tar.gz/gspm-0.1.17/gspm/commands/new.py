
import logging
import argparse
import os
import base64
from argparse import ArgumentParser
import gspm.utils.path_utils as path_utils
from cookiecutter.main import cookiecutter


def _run(project):
    logging.debug("[New] _run")
    if project.args.template:
        logging.debug("- using template [{0}]".format(project.args.template))
        dn = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../templates/" + project.args.template)
        logging.debug(dn)
        folder_name = project.args.name.replace("-", "_")
        ec = {}

        ec['project_name'] = project.args.name
        ec['folder_name'] = folder_name

        if 'general' in project.options:

            if 'author' in project.options['general']:
                ec['general_author'] = project.options['general'].get('author')

            if 'email' in project.options['general']:
                ec['general_email'] = project.options['general'].get('email')

            if 'copyright' in project.options['general']:
                ec['general_copyright'] = project.options['general'].get('copyright')

            if 'twitter' in project.options['general']:
                ec['general_twitter'] = project.options['general'].get('twitter')

            if 'license' in project.options['general']:
                ec['general_license'] = project.options['general'].get('license')

        if 'godot' in project.options:

            if 'version' in project.options['godot']:
                ec['godot_version'] = project.options['godot'].get('version')

            if 'arch' in project.options['godot']:
                ec['godot_arch'] = project.options['godot'].get('arch')

            if 'mono' in project.options['godot']:
                ec['godot_mono'] = project.options['godot'].get('mono')

        logging.debug(ec)
        cookiecutter(dn, no_input=True, extra_context=ec)
        logging.log(99, "new project {0} created".format(project.args.name))



class New:

    @staticmethod
    def run(project):
        logging.debug("[New] run")
        _run(project)

    def add_parser(self, subparser: ArgumentParser):
        logging.debug("[New] add_parser")
        logging.debug("- adding [new] command")

        cmd = subparser.add_parser("new", help="create a new Godot project")
        cmd.set_defaults(func=self.run)

        cmd.add_argument(
            "-t",
            "--template",
            dest="template",
            help="use a template",
            default="default"
        )

        cmd.add_argument(
            "name",
            help="the name of the new project",
        )

        cmd.add_argument(
            "--ignore-project",
            default=True,
            help=argparse.SUPPRESS
        )
