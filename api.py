import configparser
import os, sys
import re
from canvasapi import Canvas
from canvasapi import page

def split_page_url(url):
    """
    Retrieve API url, course id and page name from full URL
    Example URL:
    https://canvas.instance.com/courses/course_id/pages/page_name
    * API url: https://canvas.instance.com
    * course ID: course_id
    * page name: page_name
    """
    none, API_URL, course_id, page_name, none = re.split('(.*)/courses/(.*)/pages/(.*)', url)
    return API_URL, course_id, page_name

def split_folder_url(url):
    """
    Retrieve API url, course id and folder name from full URL
    Example URL:
    https://canvas.instance.com/courses/course_id/files/folder/folder_name
    * API url: https://canvas.instance.com
    * course ID: course_id
    * folder name: folder_name
    """
    none, API_URL, course_id, folder_name, none = re.split('(.*)/courses/(.*)/files/folder/(.*)', url)
    return API_URL, course_id, folder_name

def get_API(config_file_name, API_URL):
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

def get_course(API_URL, course_id, config_file):
    """
    Connects to canvas and retrieves the course.
    """
    # load configuration settings
    API_KEY = get_API(config_file, API_URL)

    # initialize a new Canvas object
    canvas = Canvas(API_URL, API_KEY)

    # get the course
    try:
        course = canvas.get_course(course_id)
    except:
        sys.exit("Could not connect to Canvas, check internet connection and/or API key in the config file %s" % config_file)

    return course

def folder_exists(course, folder_name):
    """
    Tests whether a folder exists for a course
    The folder name is everything following the 'files/folder/' in the folder's URL:

    'folder_name' in the case of this URL
    https://canvas.instance.com/courses/course_id/files/folder/folder_name

    OR

    'folder1/folder2/folder_name' in the case of this URL
    https://canvas.instance.com/courses/course_id/files/folder/folder1/folder2/folder_name
    """
    for folder in course.get_folders():
        if folder.full_name == 'course files/' + folder_name:
            return True
    return False

def find_folder(course, folder_name):
    """
    Uses folder name to find the corresponding folder
    """
    for folder in course.get_folders():
        if folder.full_name == 'course files/' + folder_name:
            return folder
