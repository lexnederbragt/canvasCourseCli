import os, sys
import configparser
from canvasapi import Canvas
from canvasapi import page
import argparse
import re

def get_API(config_file_name, API_URL):# canvas_instance, course_id, config_file_name):
    """
    Parse config file
    Extract correct API key
    """

    config = configparser.ConfigParser()
    result = config.read_file(open(os.path.expanduser(config_file_name)))
    if result == []:
        sys.exit("Error: could not open config file or config file was empty or malformed: " + config_file)
    # Canvas API key
    try:
        API_KEY = config[API_URL]['api_key']
    except KeyError:
        sys.exit("Error: could not find the entry for 'api-key' in the Canvas instance '%s' section of the config file '%s'." % (API_URL, config_file_name))

    return API_KEY


def parse_args():
    # help text and argument parser
    # solution based on https://stackoverflow.com/a/24181138/462692
    desc = '\n'.join(["To be added.",
                     "Add note about default config file '~/.config/canvasapi.conf'.\n"
                     "An optional argument -c/--config_file can be used with the path to the config file."
                      ])
    parser = argparse.ArgumentParser(description=desc)
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument("-u", "--url", help="The full url of the page to be updated", required = True)
    required_named.add_argument("-f", "--html_file", help="The name of the html file that will be sent to Canvas", required = True)
    parser.add_argument("-cf", "--config_file", help="Path to config file", default = '~/.config/canvasapi.conf')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    # split url into parts
    none, API_URL, course_id, page_name, none = re.split('(.*)/courses/(.*)/pages/(.*)', args.url)

    # load configuration settings
    API_KEY = get_API(args.config_file, API_URL)

    # Initialize a new Canvas object
    canvas = Canvas(API_URL, API_KEY)

    # get the course
    try:
        course = canvas.get_course(course_id)
    except:
        sys.exit("Could not connect to Canvas, check internet connection and/or API key in the config file %s" % args.config_file)

    # read new content
    with open(args.html_file, 'r') as html_file:
        html_content = html_file.read()#.replace('\n', '')

    # get the course page
    try:
        page_to_update = course.get_page(page_name)
    except:
        sys.exit("Error: could not find page '%s' on Canvas for updating.\nFull url: %s" % (page_name, args.url))

    # test for whether the existing page is identical to the new html file
    if page_to_update.body.split("\n")[:-1] == html_content.split("\n")[:-1]:
        print("It seems the content of the html file '%s' is identical to the current page on canvas. The update may not result in any change." % args.html_file)

    # update the course page
    api_call_result = page_to_update.edit(wiki_page = {"title":page_to_update.title, "body":html_content})

    # testing whether the update has happened
    # in which case the first part of the api_call_result is the updated html
    if html_content in api_call_result.body:
        print("Sucessfully updated page "+ args.url)
    else:
        print("Page", args.url, "appears to have been updated but new content is not identical to the html file provided...")

if __name__ == '__main__':
    main()
