#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
from xy_cli import __version__

command_name = os.path.basename(__file__).split('.', 1)[0].replace("_", ":")


def register(parser, subparsers, **kwargs):

    def handler(args):
        print("v%s" % __version__)

    subcommand = subparsers.add_parser(command_name, help='print version')
    subcommand.set_defaults(handler=handler)
