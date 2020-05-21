import sys
import argparse
from api import get_course, split_url, folder_exists

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

def create_folder(course, folder_name, folder_url):
    """
    Creates a folder on Canvas
    """
    try:
        new_folder = course.create_folder(folder_name, parent_folder_path = '/')
        # folder.full_name starts with 'course files/'
        # trial and error showed I need this to get everything after:
        # lstrip('course files')[1:]
        new_folder_name = new_folder.full_name.lstrip('course files')[1:]
        print(f"Succesfully created folder '{new_folder_name}' on Canvas.")
        print(f"Full url: {folder_url}")
        return new_folder
    except:
        sys.exit("Error: could not create folder '%s' on Canvas.\nFull url: %s" % (folder_name, args.url))

def main(args):
    args = parse_args(args)

    # extract course information from url and get course
    API_URL, course_id, folder_name = split_url(args.url, expected = 'folder')
    course =  get_course(API_URL, course_id, args.config_file)

    if not folder_exists(course, folder_name):
        new_folder = create_folder(course, folder_name, args.url)
    else:
        sys.exit("Error: folder '%s' already exists on Canvas.\nFull url: %s" % (folder_name, args.url))

if __name__ == "__main__":
    main(sys.argv[1:])
