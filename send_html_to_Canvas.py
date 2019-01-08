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
        print("Error: could not find the 'api-key' entry in for course code '%s' in the 'courses' section of the config file." %course_code)
    
    # Canvas API key
    try:
        API_KEY = config[course_code]['api_key']
    except KeyError:
        print("Error: could not find the 'api-key' entry for course code '%s' in the 'courses' section of the config file." %course_code)
    
    return API_URL, API_KEY, course_id

# these will become command line parameters
config_file = '~/.config/canvasapi.conf' # default
canvas_instance = 'uio'
course_code = 'bios1100'
html_to_send = 'api_test.html'
title_for_page = 'Testing Canvas API'


# load configuration seettings
config = read_config(config_file)
API_URL, API_KEY, course_id = get_API(config, canvas_instance, course_code)

# set some variables needed later on
# canvas uses the page title in lower case with dashes for spaces as url for the page
url_for_page = title_for_page.lower().replace(' ','-')
full_page_url = '/'.join([API_URL, 'courses', course_id, 'pages', url_for_page])

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

# get the course
course = canvas.get_course(course_id)

# read new content
with open(html_to_send, 'r') as html_file:
    html_content = html_file.read()#.replace('\n', '')

# get the course page
try:
    test_page = course.get_page(url_for_page)
except:
    sys.exit("Error: could not find page '%s' on Canvas for updating." % url_for_page)

# update the course page
api_call_result = test_page.edit(wiki_page = {"title":title_for_page, "body":html_content})

# testing whether the update has happened
# in which case the first part of the api_call_result is the updated html
if html_content in api_call_result.body:
    print("Sucessfully updated page "+ full_page_url)

