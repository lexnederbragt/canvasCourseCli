import sys
import argparse
from pathlib import Path
from api import get_course, split_url, strip_folder_name

def parse_args(args):
    # help text and argument parser
    # solution based on https://stackoverflow.com/a/24181138/462692
    desc = '\n'.join(["Downloads all files and pages for a course on Canvas.",
                     "Pages are downloaded as html files and placed in a folder called 'pages'."
                     "Files are placed in a folder called 'files'."
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

    #########
    # pages #
    #########
    pages = []
    destination_path = Path('pages/')
    if not destination_path.exists():
        destination_path.mkdir(parents=True) # cannot use `exists_ok = True`
    for page in course.get_pages():
        destination_file = "pages/" + page.url + ".html"
        print("Downloading page '" + page.title + "' to " + destination_file)
        page_to_view = course.get_page(page.url)
        page_content = page_to_view.body
        # check for empty pages, they are of type 'NoneType'
        if not page_content:
            page_content = ''
        with open(destination_file, 'w') as fh_out:
            fh_out.write(page_content.encode('utf-8'))

    #########
    # files #
    #########
    files = []
    for folder in course.get_folders():
        # remove leading '"course files/' from path
        folder_name = strip_folder_name(folder.full_name)
        # place files in a folder called 'files'
        destination = 'files/'
        if folder_name != '':
            # subfolder
            # preface with 'files' and add a trailing '/'
            destination += folder_name + "/"
        # if destination folder does not exist, create it
        # (needed because of Python 2)
        destination_path = Path(destination)
        if not destination_path.exists():
            destination_path.mkdir(parents=True) # cannot use `exists_ok = True`
        # download all files in this folder
        for file in folder.get_files():
            print("Downloading file " + destination[6:] + file.display_name + " to " + destination + file.display_name)
            file.download(destination + file.display_name)

if __name__ == "__main__":
    main(sys.argv[1:])
