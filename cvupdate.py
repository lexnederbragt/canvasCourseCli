#!/usr/bin/env python

import argparse
import sys

import update_html
import view_html
import create_folder
import add_file

# modelled after _ _ main _ _.py from
# https://github.com/dib-lab/screed/tree/master/screed
class AllCommands(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="",
            usage='''cvupdate <command> [<args>]

Available:

    update_html   -u URL -f HTML_FILE      Update the content of a page on Canvas.
    view_html     -u URL                   View the content of a page on Canvas.
    create_folder -u URL                   Create a new folder on Canvas.
    add_file      -u URL -f FILE_TO_SEND   Add a file to a folder on Canvas.

To get help on individual commands: cvupdate <command> -h

''')

        commands = {
            'update_html': update_html.main,
            'view_html': view_html.main,
            'create_folder': create_folder.main,
            'add_file': add_file.main,
        }

        parser.add_argument('command')
        args = parser.parse_args(sys.argv[1:2])
        if args.command not in commands:
            print('Unrecognized command')
            parser.print_help()
            sys.exit(1)

        cmd = commands[args.command]
        cmd(sys.argv[2:])


def main():
    AllCommands()
    return 0

if __name__ == "__main__":
    main()
