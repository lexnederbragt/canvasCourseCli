import os, sys
import configparser
# Import the Canvas class
from canvasapi import Canvas
from canvasapi import page
import re

def read_config(config_file):
    """Load config file"""
    config = configparser.ConfigParser()
    result = config.read_file(open(os.path.expanduser(config_file)))
    if result == []:
        sys.exit("Error: could not open config file or config file was empty or malformed: " + config_file)
    return config

def get_API(config, config_file_name):# canvas_instance, course_id, config_file_name):
    """
    Parse config file
    Extract correct API key
    """

    # Canvas API key
    try:
        API_KEY = config['uio']['api_key']
    except KeyError:
        sys.exit("Error: could not find the entry for 'api-key' in the Canvas instance '%s' section of the config file '%s'." % (canvas_instance, config_file_name))

    return API_KEY

import argparse
# help text and argument parser
# solution based on https://stackoverflow.com/a/24181138/462692
desc = '\n'.join(["To be added.",
                 "Add note about default config file '~/.config/canvasapi.conf'.\n"
                 "An optional argument -c/--config_file can be used with the path to the config file."
                  ])
parser = argparse.ArgumentParser(description=desc)
required_named = parser.add_argument_group('required named arguments')
#required_named.add_argument("-i", "--instance", help="The name of the Canvas instance as defined in the config file", required = True)
#required_named.add_argument("-c", "--course_id", help="The relevant course id (number) used in the course's url, the part following '/courses/' ", required = True)
#required_named.add_argument("-p", "--page_name", help="The last part of the url of the page to be updated, the part following '/pages/'", required = True)
required_named.add_argument("-u", "--url", help="The full url of the page to be updated", required = True)
required_named.add_argument("-f", "--html_file", help="The name of the html file that will be sent to Canvas", required = True)
parser.add_argument("-cf", "--config_file", help="Path to config file", default = '~/.config/canvasapi.conf')
args = parser.parse_args()

# load configuration settings
config = read_config(args.config_file)
API_KEY = get_API(config, args.config_file)

# split url into parts
none, API_URL, course_id, page_name, none = re.split('(.*)/courses/(.*)/pages/(.*)', args.url)

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

# get the course
course = canvas.get_course(course_id)

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


# title_for_page = 'Testing Canvas API'
# canvas uses the page title in lower case with dashes for spaces as url for the page
# page_name = 'testing-canvas-api' # title_for_page.lower().replace(' ','-')
