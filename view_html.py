import sys
import argparse
from api import get_course, split_url


def parse_args(args):
    # help text and argument parser
    # solution based on https://stackoverflow.com/a/24181138/462692
    desc = '\n'.join(["Command view_html not yet implemented."])
    parser = argparse.ArgumentParser(description=desc)
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument("-u", "--url", help="The full url of the page for viewing", required = True)
    parser.add_argument("-cf", "--config_file", help="Path to config file", default = '~/.config/canvasapi.conf')
    args = parser.parse_args(args)
    return args

def main(args):
    args = parse_args(args)
    page_name = split_url(args.url)[2]
    course =  get_course(args.url, args.config_file)

    # get the course page
    try:
        page_to_view = course.get_page(page_name)
    except:
        sys.exit("Error: could not find page '%s' on Canvas for viewing.\nFull url: %s" % (page_name, args.url))

    # print the page
    print(page_to_view.body)

if __name__ == "__main__":
    main(sys.argv[1:])
