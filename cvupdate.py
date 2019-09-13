#!/usr/bin/env python

import argparse
import sys

import update_page
import view_page
import create_folder
import add_file
import add_to_module

# modelled after _ _ main _ _.py from
# https://github.com/dib-lab/screed/tree/master/screed
class AllCommands(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="",
            usage='''cvupdate.py <command> [<args>]

Available:

    update_page   -u URL -f HTML_FILE      Update the content of a page on Canvas.
    view_page     -u URL                   View the content of a page on Canvas.
    create_folder -u URL                   Create a new folder on Canvas.
    add_file      -u URL -f FILE_TO_SEND   Add a file to a folder on Canvas.
    add_to_module -u URL -m MODULE_NAME    Add a page on Canvas to a module.

To get help on individual commands: cvupdate <command> -h

''')

        commands = {
            'update_page': update_page.main,
            'view_page': view_page.main,
            'create_folder': create_folder.main,
            'add_file': add_file.main,
            'add_to_module': add_to_module.main
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
