import sys
import argparse
from api import get_course, split_folder_url, find_folder

def parse_args(args):
    # help text and argument parser
    # solution based on https://stackoverflow.com/a/24181138/462692
    desc = '\n'.join(["Uplaods a file to a folder on canvas.",
                     "An optional argument -c/--config_file can be used with the path to the config file. "
                     "Otherwise the default config file '~/.config/canvasapi.conf' will be used.\n"
                      ])
    parser = argparse.ArgumentParser(description=desc)
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument("-u", "--url", help="The full url of the folder where the file will be uploaded to.", required = True)
    required_named.add_argument("-f", "--file_to_send", help="The name of the file that will be uploaded to Canvas", required = True)
    parser.add_argument("-cf", "--config_file", help="Path to config file", default = '~/.config/canvasapi.conf')
    args = parser.parse_args(args)
    return args

def main(args):
    args = parse_args(args)

    # split url into parts
    API_URL, course_id, folder_name = split_folder_url(args.url)
    course =  get_course(API_URL, course_id, args.config_file)

    folder = find_folder(course, folder_name)
    if not folder:
        sys.exit("Could not find folder '%s'. Full url: %s" %(folder_name, args.url))

    folder.upload(args.file_to_send)




if __name__ == "__main__":
    main(sys.argv[1:])
