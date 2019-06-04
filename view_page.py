import sys
import argparse
from api import get_course, split_page_url


def parse_args(args):
    # help text and argument parser
    # solution based on https://stackoverflow.com/a/24181138/462692
    desc = '\n'.join(["Shows the html content of an existing page on canvas.",
                     "An optional argument -c/--config_file can be used with the path to the config file. "
                     "Otherwise the default config file '~/.config/canvasapi.conf' will be used.\n"
                      ])
    parser = argparse.ArgumentParser(description=desc)
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument("-u", "--url", help="The full url of the page for viewing", required = True)
    parser.add_argument("-cf", "--config_file", help="Path to config file", default = '~/.config/canvasapi.conf')
    args = parser.parse_args(args)
    return args

def main(args):
    args = parse_args(args)
    API_URL, course_id, page_name = split_page_url(args.url)
    course =  get_course(API_URL, course_id, args.config_file)

    # get the course page
    try:
        page_to_view = course.get_page(page_name)
    except:
        sys.exit("Error: could not find page '%s' on Canvas for viewing.\nFull url: %s" % (page_name, args.url))

    # print the page
    print(page_to_view.body)

if __name__ == "__main__":
    main(sys.argv[1:])
