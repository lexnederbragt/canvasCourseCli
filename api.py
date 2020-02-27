import configparser
import os, sys
import re
from canvasapi import Canvas
from canvasapi import page

def split_url(url, expected):
    """
    Retrieve API url, course id from full URL
    Determine url type and compare to expected
    Current url types: folder name, page name, url only

    Example URL:
    https://canvas.instance.com/courses/course_id/pages/page_name
    https://canvas.instance.com/courses/course_id/files/folder/folder_name
    * API url: https://canvas.instance.com
    * course ID: course_id
    * page name: page_name
    * folder name: folder_name
    """

    # split the url
    if expected in ['page', 'folder']:
        none, API_URL, course_id, rest, none = re.split(r'(.*)/courses/(\d*)/(.*)', url)
    elif expected in ['new page', 'url only']:
        none, API_URL, course_id, none = re.split(r'(.*)/courses/(\d*)', url)
        rest = 'course url'
    else:
        sys.exit("Expected url type not implemented yet: " + expected)

    # determine type
    if rest.startswith('pages/'):
        url_type = 'page'
        item_name = re.sub(r'^pages/', '', rest)
    elif rest.startswith('files/folder/'):
        url_type = 'folder'
        item_name = re.sub(r'^files/folder/', '', rest)
    elif rest == 'course url' and expected == 'new page':
        url_type = 'new page'
        item_name = ''
    elif rest == 'course url' and expected == 'url only':
        url_type = 'url only'
        item_name = ''
    else:
        sys.exit("Unexpected url: not of type 'folder' or 'page' " + url)

    # compare to expected
    if url_type != expected:
        sys.exit("Unexpected type url: expected url of type '%s', got type '%s': " \
        %(expected, url_type) + url)

    return API_URL, course_id, item_name

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

def find_module(course, module_name):
    """
    Uses module name to find the corresponding module
    """
    for module in course.get_modules():
        if module.name == module_name:
            return module

def strip_folder_name(long_folder_name):
    """
    Removes leading '"course files/' from folder 'path'
    """
    return long_folder_name[13:]
