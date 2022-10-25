import sys
import argparse
import os.path
from api import get_course, split_url, find_module, page_exists, get_file
from add_module import create_module, get_module_url, publish_module

def parse_args(args):
    # help text and argument parser
    # solution based on https://stackoverflow.com/a/24181138/462692
    desc = '\n'.join(["Adds an existing file or page on Canvas, or a hyperlink, \
                      to a module in the same course.",
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
    parser.add_argument("-lt", "--linktitle", help="The title (name) of the link to be added, enclosed in quotation marks if it \
    contains one or more spaces.")
    parser.add_argument("-lu", "--linkurl", help="The URL (hyperlink address) of the link to be added.")
    parser.add_argument("-ext", "--externaltool", help="Add the URL as an \
                        External Tool (defaul: add as a regular hyperlink).", action='store_true')
    parser.add_argument("--create", help="If the module does not exist yet, \
    create it before adding the page (default: off, and warn instead)", action='store_true')
    parser.add_argument("-p", "--publish", help="Publish the module on Canvas \
    at the time of creation (default: leave unpublished)", action='store_true')
    parser.add_argument("--force", help="If the page has already been added, \
    add it another time to the module anyway (default: off)", action='store_true')
    parser.add_argument("--ignore", help="If the page has already been added, \
    ignore this fact and exit without error (default: off)", action='store_true')
    parser.add_argument("-cf", "--config_file", help="Path to config file", \
        default = '~/.config/canvasapi.conf')
    args = parser.parse_args(args)
    return args


def item_is_added_to_module(module, item, item_id,  url_type):
    """
    Tests whether an item has already been added to a module
    item is a page or a file.
    """
    for module_item in module.get_module_items():
        # module_item.type is capitalised
        module_item_type = module_item.type.lower()
        # only compare items of same type
        if module_item_type == url_type:
            if module_item_type == 'page':
                # pages have a unique title
                module_item_id = module_item.title
                # compare the IDs
                if module_item.title == item_id:
                    return True
            else:
                # files have a unique ID,
                # which for a file in a module is the content_id
                module_item_id = module_item.content_id
                # compare the IDs
                if module_item_id == item_id:
                    return True
    return False

def main(args):
    args = parse_args(args)

    # extract course information from url and get course
    API_URL, course_id, item_name, url_type = split_url(args.url)

    course =  get_course(API_URL, course_id, args.config_file)

    if url_type == 'page':
        # check whether page to add actually exists
        # if so, get it
        if page_exists(course, item_name):
            item_to_add = course.get_page(item_name)
            # pages have a unique title
            item_id = item_to_add.title
        else:
            sys.exit("Error: could not find page '%s' on Canvas.\nFull url: %s" % (item_name, args.url))

    elif url_type == 'file':
        # get file to add if it actually exists
        # if not, becomes False
        item_to_add = get_file(course, item_name)
        if not item_to_add:
            sys.exit("Error: could not find file '%s' on Canvas.\nFull url: %s" % (item_name, args.url))
        # files have a unique ID
        item_id = item_to_add.id
    elif url_type == "url only" and args.linkurl:
        pass
        #sys.exit([API_URL, course_id, item_name, url_type, args.linkurl, args.linktitle])
    else:
        sys.exit(f"Error: unexpected type of item to add: '{url_type}', expected 'file' or 'page': {args.url}")

    module_name = args.title
    # find the module
    module = find_module(course, module_name)
    if not module:
        # module does not exist
        if not args.create:
            sys.exit("Could not find module '%s' on Canvas" % module_name)
        else:
            # create module, publish if requested
            module = create_module(course, module_name)
            module_url = get_module_url(module.items_url)
            print(f"Sucessfully added module '{module.name}'. Full url: {module_url}.")
            if args.publish:
                publish_module(module)

    if url_type in ['page', 'file']:
        # check whether page already added to module
        if item_is_added_to_module(module, item_to_add, item_id, url_type):
            if not args.force and not args.ignore:
                message = f"Error: {url_type} '{item_name}' "
                message += f"already added to module '{module.name}'.\n"
                message += "To add anyway, use '--force'\n"
                sys.exit(message)
            elif args.ignore:
                message = f"Warning: {url_type} '{item_name}' "
                message += f"already added to module '{module.name}'.\n"
                message += "Ignoring...\n"
                print(message)
                sys.exit(0)

    # update the module
    if url_type == 'page':
        try:
            # not sure what to add for content_id but "" works
            new_module_item = module.create_module_item(module_item = {
                "type" : "Page",
                "content_id" : "",
                "page_url": item_to_add.url
                })
            print("Sucessfully added page '%s' to module '%s'." %(item_name, module_name))
        except Exception as e:
            sys.exit("Could not add page '%s' to module '%s':\n%s." %(item_name, module_name, str(e)))

    elif url_type == 'file':
        try:
            new_module_item = module.create_module_item(module_item = {
                "type" : "File",
                "content_id":item_to_add.id,
                })
            print("Sucessfully added file '%s' to module '%s'." %(item_name, module_name))
        except Exception as e:
            sys.exit("Could not add file '%s' to module '%s':\n%s." %(item_name, module_name, str(e)))

    elif url_type == "url only" and args.linkurl:
        module_item = {
            "title" : args.linktitle,
            "external_url" : args.linkurl,
            "new_tab" : True,
            }
        if args.externaltool:
            # not sure what to add for content_id but "" works
            module_item["type"] = "ExternalTool"
            module_item["content_id"] = ""
        else:
            module_item["type"] = "ExternalUrl"
        try:
            new_module_item = module.create_module_item(module_item = module_item)
            print("Sucessfully added url '%s' with title '%s' to module '%s'." %(args.linkurl, args.linktitle, module_name))
        except Exception as e:
            sys.exit("Could not add url '%s' to module '%s':\n%s." %(args.linkurl, module_name, str(e)))

if __name__ == "__main__":
    main(sys.argv[1:])
