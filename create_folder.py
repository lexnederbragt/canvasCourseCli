import sys
import argparse
from api import get_course, split_folder_url, folder_exists

def parse_args(args):
    # help text and argument parser
    # solution based on https://stackoverflow.com/a/24181138/462692
    desc = '\n'.join(["Creates a new folder on canvas.",
                     "An optional argument -c/--config_file can be used with the path to the config file. "
                     "Otherwise the default config file '~/.config/canvasapi.conf' will be used.\n"
                      ])
    parser = argparse.ArgumentParser(description=desc)
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument("-u", "--url", help="The full url of the folder to be created", required = True)
    parser.add_argument("-cf", "--config_file", help="Path to config file", default = '~/.config/canvasapi.conf')
    args = parser.parse_args(args)
    return args

def main(args):
    args = parse_args(args)

    # split url into parts
    API_URL, course_id, new_folder_name = split_folder_url(args.url)
    course =  get_course(API_URL, course_id, args.config_file)

    if not folder_exists(course, new_folder_name):
        try:
            course.create_folder(new_folder_name, parent_folder_path = '/')
            print("Succesfully created folder '%s' on Canvas.")
            print("Full url: %s" % (new_folder_name, args.url))
        except:
            sys.exit("Error: could not create folder '%s' on Canvas.\nFull url: %s" % (new_folder_name, args.url))
    else:
        sys.exit("Error: folder '%s' already exists on Canvas.\nFull url: %s" % (new_folder_name, args.url))




if __name__ == "__main__":
    main(sys.argv[1:])
