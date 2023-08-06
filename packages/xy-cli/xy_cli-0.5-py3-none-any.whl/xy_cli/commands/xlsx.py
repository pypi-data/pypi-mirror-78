#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ..libs.XlsxLoader import XlsxLoader
import sys, os
import pprint
import argparse

command_name = os.path.basename(__file__).split('.', 1)[0].replace("_", ":")


def main(args):

    data = XlsxLoader().load_data(args.file,
                                  args.sheet,
                                  header_row=args.header_row,
                                  header_col=args.header_col,
                                  end_row=args.end_row,
                                  end_col=args.end_col)
    if args.debug:
        print("filter_title: %s" % args.filter_title)
        print("filter: %s" % args.filter)
        print("header: %s" % ",".join(data[0].keys()))
        print("first-row: %s" % ",".join(data[1].values()))

    if args.filter and args.filter_title:
        data = [row for row in data if row[args.filter_title] in args.filter]

    if data is None or len(data) == 0:
        print("no data!")
        return

    result = []
    header = data[0].keys()
    if args.format is None:
        result.append(",".join(header))
    for row in data:
        if args.format:
            result.append(args.format.format(**row))
        else:
            result.append(",".join(row.values()))
    print(args.IFS.join(result), end="")


def register(parser, subparsers, **kwargs):

    def handler(args):
        if args.file is None or args.example:
            print("""hello""")
            print(parser.parse_args([command_name, '--help']))
            return
        if args.file:
            main(args)

    subcommand = subparsers.add_parser(command_name, help='excel data reader')
    subcommand.add_argument('-f',
                            '--file',
                            type=str,
                            default=None,
                            help='xlsx file',
                            required=False)
    subcommand.add_argument('-s',
                            '--sheet',
                            type=str,
                            help='sheet name',
                            required=False)
    subcommand.add_argument('--header_row',
                            type=int,
                            default=0,
                            help='header_row, default 0',
                            required=False)
    subcommand.add_argument('--header_col',
                            type=int,
                            default=0,
                            help='header_col, default 0',
                            required=False)
    subcommand.add_argument('--end_row',
                            type=int,
                            default=None,
                            help='end_row',
                            required=False)
    subcommand.add_argument('--end_col',
                            type=int,
                            default=None,
                            help='end_col',
                            required=False)
    subcommand.add_argument('--IFS',
                            type=str,
                            default='\r\n',
                            help='IFS, default CRLF',
                            required=False)
    subcommand.add_argument('--format',
                            type=str,
                            default=None,
                            help='print format for row.',
                            required=False)
    subcommand.add_argument('--filter',
                            nargs="*",
                            help='meta_type',
                            required=False)
    subcommand.add_argument('--filter_title',
                            type=str,
                            help='filter_title',
                            default='filter',
                            required=False)
    subcommand.add_argument('--example',
                            action='store_true',
                            help='print usage example',
                            required=False)
    subcommand.add_argument('--debug',
                            action='store_true',
                            help='debug',
                            required=False)
    subcommand.set_defaults(handler=handler)
