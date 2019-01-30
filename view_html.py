import argparse
import sys

def main(args):

    def parse_args(args):
        # help text and argument parser
        # solution based on https://stackoverflow.com/a/24181138/462692
        desc = '\n'.join(["Command view_html not yet implemented."])
        parser = argparse.ArgumentParser(description=desc)
#        parser.add_argument("-cf", "--config_file", help="Path to config file", default = '~/.config/canvasapi.conf')
        args = parser.parse_args(args)
        return args


    args = parse_args(args)
    print("Command view_html not yet implemented.")

if __name__ == "__main__":
    main(sys.argv[1:])
