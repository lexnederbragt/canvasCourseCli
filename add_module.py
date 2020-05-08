import sys
import argparse
from api import get_course, split_url, module_exists
from list_modules import get_module_url

def parse_args(args):
    # help text and argument parser
    # solution based on https://stackoverflow.com/a/24181138/462692
    desc = '\n'.join(["Add a new module to Canvas.",
                     "An optional argument -c/--config_file can be used with the path to the config file. "
                     "Otherwise the default config file '~/.config/canvasapi.conf' will be used.\n"
                      ])
    parser = argparse.ArgumentParser(description=desc)
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument("-u", "--url", help="The url of the course, ending with the course id", required = True)
    required_named.add_argument("-t", "--title", help="The title (name) of the module to be added, enclosed in quotation marks if it \
    contains one or more spaces.", required = True)
    parser.add_argument("-p", "--publish", help="Publish the module on Canvas at the time of creation (default: leave unpublished)", action='store_true')
#    parser.add_argument("--force", help="If the module is already present, create the module anyway (default: off)", action='store_true')
    parser.add_argument("-cf", "--config_file", help="Path to config file", default = '~/.config/canvasapi.conf')
    args = parser.parse_args(args)
    return args

def create_module(course, title):
    new_module = course.create_module(module = {
        "name":title,
        })
    return new_module

def main(args):
    args = parse_args(args)

    # check whether module needs to be published
    published = 'false'
    if args.publish:
        published = 'true'

    # extract course information from url and get course
    API_URL, course_id, new_module_name = split_url(args.url, expected = 'url only')
    course =  get_course(API_URL, course_id, args.config_file)

    # test whether module exists
    # new_module_name = args.title.lower().replace(" ","-")
    # if module_exists(course, new_module_name) and not args.force:
    #     message ="Error: module with name '{}' already exists on Canvas.\n".format(new_module_name)
    #     message += "Full url: {}\n".format(args.url)
    #     message += "To create anyway, use '--force'\n"
    #     sys.exit(message)

    # update the course module
    new_module = create_module(course, args.title)
    new_module_url = get_module_url(new_module.items_url)
    print(f"Sucessfully added module '{new_module.name}'. Full url: {new_module_url}.")

if __name__ == "__main__":
    main(sys.argv[1:])
