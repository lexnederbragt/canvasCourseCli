import sys
import argparse
import os.path
from api import get_course, split_folder_url, find_folder

def parse_args(args):
    # help text and argument parser
    # solution based on https://stackoverflow.com/a/24181138/462692
    desc = '\n'.join(["Uploads a file to a folder on canvas, overwriting the existing file if present.",
                     "An optional argument -c/--config_file can be used with the path to the config file. "
                     "Otherwise the default config file '~/.config/canvasapi.conf' will be used.\n"
                      ])
    parser = argparse.ArgumentParser(description=desc)
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument("-u", "--url", help="The full url of the folder where the file will be uploaded to.", required = True)
    required_named.add_argument("-f", "--file_to_send", help="The path to the file that will be uploaded to Canvas", required = True)
    parser.add_argument("-cf", "--config_file", help="Path to config file", default = '~/.config/canvasapi.conf')
    args = parser.parse_args(args)
    return args

def main(args):
    args = parse_args(args)

    # check whether file to upload actually exists
    if not os.path.isfile(args.file_to_send):
        sys.exit("Error: could not find file '%s'" % args.file_to_send)

    # split url into parts
    API_URL, course_id, folder_name = split_folder_url(args.url)
    course =  get_course(API_URL, course_id, args.config_file)

    # find the folder
    folder = find_folder(course, folder_name)
    if not folder:
        sys.exit("Could not find folder '%s'. Full url: %s" %(folder_name, args.url))

    # do the upload and capture the return
    result = folder.upload(args.file_to_send)
    # first key is True when successful
    if result[0]:
        print("Succesfully uploaded file '%s' to folder '%s'.\nFull url: %s" \
        % (args.file_to_send, folder_name, args.url + '/' + args.file_to_send))
    else:
        sys.exit("Could not upload file '%s' to folder '%s'.\nFull url: %s" \
        % (args.file_to_send, folder_name, args.url + '/' + args.file_to_send))

if __name__ == "__main__":
    main(sys.argv[1:])
