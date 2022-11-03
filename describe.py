import sys
import argparse
from pathlib import Path
from api import get_course, split_url, strip_folder_name

def parse_args(args):
    # help text and argument parser
    # solution based on https://stackoverflow.com/a/24181138/462692
    desc = '\n'.join(["Describe the elements of a course.",
                     "...",
                     "An optional argument -c/--config_file can be used with the path to the config file. "
                     "Otherwise the default config file '~/.config/canvasapi.conf' will be used.\n"
                      ])
    parser = argparse.ArgumentParser(description=desc)
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument("-u", "--url", help="The url of the course, ending with the course id", required = True)
    parser.add_argument("-cf", "--config_file", help="Path to config file", default = '~/.config/canvasapi.conf')
    args = parser.parse_args(args)
    return args

def is_published_txt(published):
    if published:
        return "Published"
    else:
        return "Unpublished"

def describe_module(module):
    """
    Extracts information from all items asssociated
    with a module and prints them.
    """
    for module_item in module.get_module_items():
        item_data = []
        # collect defaults
        item_data.append(module_item.type)
        item_data.append(module_item.title)
        item_data.append(module_item.position)
        item_data.append(is_published_txt(module_item.published))
        if module_item.type != "SubHeader":
            item_data.append(module_item.html_url)
        elif module_item.type in ["ExternalUrl", "ExternalTool"]:
            item_data.append(module_item.external_url)
        elif module_item.type in ['File', 'Discussion', 'Assignment', 'Quiz', 'ExternalTool']:
            # these have a another ID, the content_id
            item_data.append(module_item.content_id)
        print("\t", "\t".join([str(item) for item in item_data]))

def main(args):
    args = parse_args(args)

    # extract course information from url and get course
    API_URL, course_id, item_name, url_type = split_url(args.url)

    course =  get_course(API_URL, course_id, args.config_file)

    # find the module, if any
    for module in course.get_modules():
        print(module.name, module.position, is_published_txt(module.published), module.id)
        describe_module(module)


if __name__ == "__main__":
    main(sys.argv[1:])
