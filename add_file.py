import sys
import argparse
import os.path
from api import get_course, split_url, find_folder
from create_folder import create_folder

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
    parser.add_argument("--create", help="If the destination folder does not yet exists, \
    create it before adding the file (default: off, and warn instead)", action='store_true')
    parser.add_argument("-cf", "--config_file", help="Path to config file", default = '~/.config/canvasapi.conf')
    args = parser.parse_args(args)
    return args

def main(args):
    args = parse_args(args)

    # check whether file to upload actually exists
    if not os.path.isfile(args.file_to_send):
        sys.exit("Error: could not find file '%s'" % args.file_to_send)

    # extract course information from url and get course
    API_URL, course_id, folder_name = split_url(args.url, expected = 'folder')
    course =  get_course(API_URL, course_id, args.config_file)

    # find the folder
    folder = find_folder(course, folder_name)
    if not folder:
        message = f"Could not find folder '{folder_name}'\n"
        if not args.create:
            message += "Use --create to create the folder before adding the file.\n"
            message += f"Full url: {args.url}"
            sys.exit(message)
        else:
            message += "Will attempt to create the folder."
            print(message)
            folder = create_folder(course, folder_name, args.url)

    # do the upload and capture the return
    result = folder.upload(args.file_to_send)
    # first key is True when successful
    if result[0]:
        # extract file id from API call results
        file_id = result[1]['id']
        print("Succesfully uploaded file '%s' to folder '%s'.\nFull url: %s" \
        % (args.file_to_send, folder_name, args.url + '/?preview=' + str(file_id)))


    else:
        sys.exit("Could not upload file '%s' to folder '%s'.\nFull url: %s" \
        % (args.file_to_send, folder_name, args.url + '/' + args.file_to_send))

if __name__ == "__main__":
    main(sys.argv[1:])
