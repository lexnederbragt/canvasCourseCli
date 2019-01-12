import os, sys
import configparser
# Import the Canvas class
from canvasapi import Canvas
from canvasapi import page

def read_config(config_file):
    """Load config file"""
    config = configparser.ConfigParser()
    result = config.read_file(open(os.path.expanduser(config_file)))
    if result == []:
        sys.exit("Error: could not open config file or config file was empty or malformed: " + config_file)
    return config

def get_API(config, canvas_instance, course_code):
    """
    Parse config file
    Extract correct API information
    """
    # Canvas API URL
    try:
        API_URL = config['api_url'][canvas_instance]
    except KeyError:
        print("Error: could not find the entry for Canvas instance '%s' in the 'api_url' section of the config file." %canvas_instance)

    # Course ID
    try:
        course_id = config[course_code]['course_id']
    except KeyError:
        print("Error: could not find the 'course_id' entry in for course code '%s' in the 'courses' section of the config file." %course_code)
        exit(0)

    # Canvas API key
    try:
        API_KEY = config[course_code]['api_key']
    except KeyError:
        print("Error: could not find the 'api-key' entry for course code '%s' in the 'courses' section of the config file." %course_code)
        exit(0)

    return API_URL, API_KEY, course_id

# these will become command line parameters
config_file = '~/.config/canvasapi.conf' # default
#canvas_instance = 'uio'
#course_code = 'bios1100'
#html_to_send = 'api_test.html'
#title_for_page = 'Testing Canvas API'
# canvas uses the page title in lower case with dashes for spaces as url for the page
#url_for_page = 'testing-canvas-api' # title_for_page.lower().replace(' ','-')

import argparse
# help text and argument parser
desc = '\n'.join(["To be added.",
                 "Add note about default config file '~/.config/canvasapi.conf'"
                 "An optional argument -c/--config_file can be used with the path to the config file."
                  ])
parser = argparse.ArgumentParser(description=desc)
parser.add_argument("instance", help="The name of the Canvas instance as defined in the config file")
parser.add_argument("course_code", help="The relevant course code as defined in the config file")
parser.add_argument("url", help="The last part of the url of the page to de updated, the part following '/pages/'")
parser.add_argument("html_file", help="The name of the html file that will be sent to Canvas")
parser.add_argument("-c", "--config_file", help="Path to config file")
parser.add_argument("-s", "--show_config", help="Show the content of the config file", action="store_true")
args = parser.parse_args()

# load configuration seettings
config = read_config(config_file)
API_URL, API_KEY, course_id = get_API(config, args.instance, args.course_code)

# set some variables needed later on
full_page_url = '/'.join([API_URL, 'courses', course_id, 'pages', args.url])

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

# get the course
course = canvas.get_course(course_id)

# read new content
with open(args.html_file    , 'r') as html_file:
    html_content = html_file.read()#.replace('\n', '')

# get the course page
try:
    page_to_update = course.get_page(args.url)
except:
    sys.exit("Error: could not find page '%s' on Canvas for updating." % args.url)

# update the course page
api_call_result = page_to_update.edit(wiki_page = {"title":page_to_update.title, "body":html_content})

# testing whether the update has happened
# in which case the first part of the api_call_result is the updated html
if html_content in api_call_result.body:
    print("Sucessfully updated page "+ full_page_url)
