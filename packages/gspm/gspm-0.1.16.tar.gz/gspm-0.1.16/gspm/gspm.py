# pylint: disable=E501

# Copyright (C) 2018 Paul Hocker <paul@spocker.net>
# See LICENSE file for License Information

""""Godot Stuff Project Manager"""

import logging
import gspm
import sys
import dotmap
import io
import os

import gspm.parser as parser
import gspm.project as project
import gspm.utils.path_utils as path_utils
import gspm.options as options

logging_level = logging.WARN


def _get_logging_level():
    return logging_level


def init():
    '''
    Initialize the Environment

    Used to setup the Logging Environment and
    some other things for the runtime.
    '''

    logging.basicConfig(level=logging_level, format='%(message)s')

    # add file logging
    if "--log" in sys.argv:
        logging.getLogger().addHandler(logging.FileHandler(
            "./gspm.log", 
            format='[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)',
            datefmt='%m/%d/%Y %I:%M:%S %p')
        )

    # add console logging
    # logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    #   some diagnostic info
    logging.debug(sys.path)


def welcome():

    logging.log(99, "")

    #   show the logo if desired
    if logging_level < logging.ERROR:
        logging.log(99, gspm.__logo__)

    #   a little welcome message (always shown)
    logging.log(99, gspm.__name__)
    logging.log(99, "Version {0}, {1}".format(get_version(), gspm.__copyright__))


def get_version():
    '''
    Return the Version
    '''
    return gspm.__version__


def run():
    '''
    Runs the Command
    '''

    global logging_level

    try:

        print(sys.argv)

        init()

        logging.log(99, "")

        if "--quiet" in sys.argv:
            logging_level = logging.CRITICAL

        if "--verbose" in sys.argv:
            logging_level = logging.INFO

        if "--more-verbose" in sys.argv:
            logging_level = logging.DEBUG

        logging.getLogger().setLevel(logging_level)

        welcome()

        args = parser.create_parser().parse_args()

        the_project = dotmap.DotMap()

        # adjust for when path argument is added
        if hasattr(args, 'path'):
            logging.debug('path = {0}'.format(args.path))
            args.config = "{0}{1}{2}".format(args.path, os.path.sep, args.config)

        # logging.debug("args.command = {0}".format(args.command))
        # if args.command == 'edit':
        #     logging.debug(args)
        #     logging.debug("args.path = {0}".format(args.path))
        #     logging.debug("args.config = {0}".format(args.config))
        #     args.config = "{0}\{1}".format(args.path, args.config)

        the_project.options = options.load(the_project)

        #   store the args for later
        the_project.args = args

        if not args.ignore_project:

            # load config
            the_project.config = project.load(args.config)

            # get home path (aka where am i running from?)
            path_utils.define_project_paths(the_project)

        # execute
        args.func(the_project)

        #   good-bye
        sys.exit(0)

    except Exception as e:
        logging.error(e)
        logging.error("operation cancelled")
        sys.exit(1)
