import sys
import argparse
import os.path
from api import get_course, split_url, find_module
from add_module import create_module, get_module_url, publish_module

def parse_args(args):
    # help text and argument parser
    # solution based on https://stackoverflow.com/a/24181138/462692
    desc = '\n'.join(["Adds an existing page on Canvas to an existing module in the same course.",
                     "An optional argument -c/--config_file can be used with the path to the config file. "
                     "Otherwise the default config file '~/.config/canvasapi.conf' will be used.\n"
                     ])
    parser = argparse.ArgumentParser(description=desc)
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument("-u", "--url", help="The full url of the page \
        on Canvas that will be added to the module.", required = True)
    required_named.add_argument("-t", "--title", help="The title (name) of the \
        module that will be updated, enclosed in quotation marks if it \
        contains one or more spaces", required = True)
    parser.add_argument("--create", help="If the module does not exist yet, \
    create it before adding the page (default: off, and warn instead)", action='store_true')
    parser.add_argument("-p", "--publish", help="Publish the module on Canvas \
    at the time of creation (default: leave unpublished)", action='store_true')
    parser.add_argument("--force", help="If the page has already been added, \
    add it another time to the module anyway (default: off)", action='store_true')
    parser.add_argument("-cf", "--config_file", help="Path to config file", \
        default = '~/.config/canvasapi.conf')
    args = parser.parse_args(args)
    return args


def page_is_added_to_module(module, page):
    """
    Tests whether a page has already been added to a module
    """
    for module_item in module.get_module_items():
        if module_item.title == page.title:
            return True
    return False

def main(args):
    args = parse_args(args)

    # extract course information from url and get course
    API_URL, course_id, page_name = split_url(args.url, expected = 'page')
    course =  get_course(API_URL, course_id, args.config_file)

    # check whether page to add actually exists
    try:
        page_to_add = course.get_page(page_name)
    except:
        sys.exit("Error: could not find page '%s' on Canvas.\nFull url: %s" % (page_name, args.url))

    # find the module
    module = find_module(course, args.title)
    if not module:
        # module does not exist
        if not args.create:
            sys.exit("Could not find module '%s' on Canvas" % args.title)
        else:
            # create module, publish if requested
            module = create_module(course, args.title)
            module_url = get_module_url(module.items_url)
            print(f"Sucessfully added module '{module.name}'. Full url: {module_url}.")
            if args.publish:
                publish_module(module)

    # check whether page already added to module
    if page_is_added_to_module(module, page_to_add) and not args.force:
        message = f"Page '{page_to_add.title}' "
        message += f"already added to module '{module.name}'.\n"
        message += "To add anyway, use '--force'\n"
        sys.exit(message)

    # update the module
    try:
        new_module_item = module.create_module_item(module_item = {
            "type":"Page",
            "content_id":"",
            "page_url": page_to_add.url
            })
        print("Sucessfully added page '%s' to module '%s'." %(page_name, args.title))
    except Exception as e:
        sys.exit("Could not add page '%s' to module '%s':\n%s." %(page_name, args.title, str(e)))

if __name__ == "__main__":
    main(sys.argv[1:])
