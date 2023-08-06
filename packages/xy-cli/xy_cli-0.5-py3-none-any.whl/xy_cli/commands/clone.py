#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
from xy_cli.libs.FileUtil import FileUtil

command_name = os.path.basename(__file__).split('.', 1)[0].replace("_", ":")


def register(parser, subparsers, **kwargs):

    def handler(args):
        if args.from_dir:
            print("start to clone...")
            format_data = {}
            if args.data:
                for d in args.data:
                    d1 = d.split('=')
                    format_data[d1[0]] = d1[1]
            FileUtil().clone(args.from_dir, args.to_dir, format_data)
        else:
            print(parser.parse_args([command_name, '--help']))

    subcommand = subparsers.add_parser(command_name, help='clone folder')
    subcommand.add_argument('-f',
                            '--from_dir',
                            type=str,
                            help="from directory",
                            required=True)
    subcommand.add_argument('-t',
                            '--to_dir',
                            type=str,
                            help="to directory",
                            required=True)
    subcommand.add_argument('-d',
                            '--data',
                            nargs='*',
                            help="format data",
                            required=False)
    subcommand.set_defaults(handler=handler)
