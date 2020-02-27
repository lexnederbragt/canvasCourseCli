import sys
import argparse
from api import get_course, split_url, strip_folder_name

def parse_args(args):
    # help text and argument parser
    # solution based on https://stackoverflow.com/a/24181138/462692
    desc = '\n'.join(["Lists the folders for a course on Canvas in alphabetical order.",
                     "An optional argument -c/--config_file can be used with the path to the config file. "
                     "Otherwise the default config file '~/.config/canvasapi.conf' will be used.\n"
                      ])
    parser = argparse.ArgumentParser(description=desc)
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument("-u", "--url", help="The url of the course, ending with the course id", required = True)
    parser.add_argument("-cf", "--config_file", help="Path to config file", default = '~/.config/canvasapi.conf')
    args = parser.parse_args(args)
    return args

def main(args):
    args = parse_args(args)

    # extract course information from url and get course
    API_URL, course_id, new_folder_name = split_url(args.url, expected = 'url only')
    course =  get_course(API_URL, course_id, args.config_file)

    folders = []
    for folder in course.get_folders():
        # remove leading '"course files/' from path
        folder_name = strip_folder_name(folder.full_name)
        folders.append(folder_name)
    print('\n'.join(sorted(folders, key=lambda s: s.lower())))


if __name__ == "__main__":
    main(sys.argv[1:])
