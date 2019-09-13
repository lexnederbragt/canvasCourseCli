import sys
import argparse
import os.path
from api import get_course, split_page_url, find_module

def parse_args(args):
    # help text and argument parser
    # solution based on https://stackoverflow.com/a/24181138/462692
    desc = '\n'.join(["Adds an exitsing page on Canvas to an existing module in the same course.",
                     "An optional argument -c/--config_file can be used with the path to the config file. "
                     "Otherwise the default config file '~/.config/canvasapi.conf' will be used.\n"
                     ])
    parser = argparse.ArgumentParser(description=desc)
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument("-u", "--url", help="The full url of the page \
        on Canvas that will be added to the module.", required = True)
    required_named.add_argument("-m", "--module_name", help="The name of the \
        module that will be updated, enclosed in quotation marks if it \
        contains one or more spaces", required = True)
    parser.add_argument("-cf", "--config_file", help="Path to config file", \
        default = '~/.config/canvasapi.conf')
    args = parser.parse_args(args)
    return args

def main(args):
    args = parse_args(args)

    API_URL, course_id, page_name = split_page_url(args.url)

    # get the course
    course =  get_course(API_URL, course_id, args.config_file)

    # check whether page to add actually exists
    try:
        page_to_add = course.get_page(page_name)
    except:
        sys.exit("Error: could not find page '%s' on Canvas.\nFull url: %s" \% (page_name, args.url))

    # find the module
    module = find_module(course, args.module_name)
    if not module:
        sys.exit("Could not find module '%s' on Canvas" % args.module_name)

    # update the module
    try:
        api_call_result = module.create_module_item(module_item = {
            "type":"Page",
            "content_id":"",
            "page_url": page_to_add.url
            })
        print("Sucessfully added page '%s' to module '%s'." %(page_name, args.module_name))
    except Exception, e:
        sys.exit("Could not add page '%s' to module '%s':\n%s." %(page_name, args.module_name, str(e)))

if __name__ == "__main__":
    main(sys.argv[1:])
