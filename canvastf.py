#!/usr/bin/env python

import argparse
import sys

import send_html
import view_html

# modelled after _ _ main _ _.py from
# https://github.com/dib-lab/screed/tree/master/screed
class AllCommands(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="",
            usage='''canvastf <command> [<args>]

Available:

    send_html -u URL -f HTML_FILE  Update the content of a page on Canvas.
    view_html -u URL               View the content of a page on Canvas.

''')

        commands = {
            'send_html': send_html.main,
            'view_html': view_html.main,
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
