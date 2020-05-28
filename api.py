import configparser
import os, sys
import re
from canvasapi import Canvas
from canvasapi import page

def split_url(url, expected = None):
    """
    Retrieve API url, course id from full URL
    Determine url type and optionally compare to expected
    Current url types: folder name, file name, page name, url only
    Assumes only files have a dot in their name, not folders

    Example URL:
    https://canvas.instance.com/courses/course_id/pages/page_name
    https://canvas.instance.com/courses/course_id/files/folder/folder_name
    * API url: https://canvas.instance.com
    * course ID: course_id
    * page name: page_name
    * folder name: folder_name
    * file name: file.ext
    """

    # split the url
    # rest: the part following 'course_id'
    none, API_URL, course_id, rest, none = re.split(r'(.*)/courses/(\d*)(.*)', url)

    # determine type
    if rest.startswith('/pages/'):
        url_type = 'page'
        item_name = re.sub(r'^/pages/', '', rest)
    elif rest.startswith('/files/folder/'):
        # file or folder
        # files have a . in their name
        remainder = re.split(r'/files/folder/(.*\..*)', rest)
        if len(remainder) == 3:
            url_type = 'file'
        else:
            url_type = 'folder'
        item_name = re.sub(r'^/files/folder/', '', rest)
    elif rest == '':
        url_type = 'url only'
        item_name = ''
    else:
        sys.exit("Unexpected url: not of type 'file', 'folder' or 'page' " + url)

    # return value depends on whether a certain type was expected
    if expected:
        # check validity of expected result
        if not expected in ['page', 'folder', 'file', 'url only']:
            sys.exit("Expected url type not implemented yet: " + expected)
        elif url_type != expected:
            # compare result with expected
            sys.exit("Unexpected type url: expected url of type '%s', got type '%s': " \
            %(expected, url_type) + url)
        else:
            # all is good, return data
            return API_URL, course_id, item_name
    else:
        # no particular url type was expected, so add it to what is returned
        return API_URL, course_id, item_name, url_type

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

def page_exists(course, page_name):
    """
    Tests whether a page exists for a course
    The page url is everything following the 'pages/' in the pages's URL:

    'page_name' in the case of this URL
    https://canvas.instance.com/courses/course_id/pages/page_name
    """
    for page in course.get_pages():
        if page.url == page_name:
            return True
    return False

def module_exists(course, module_name):
    """
    Tests whether a module exists for a course
    Looks for an existing module of the same name.
    Returns the 'items_url' of the existing module
    or an empty string if it does not yet exists.
    """
    for module in course.get_modules():
        if module.name == module_name:
            return module.items_url
    return ''

def strip_folder_name(long_folder_name):
    """
    Removes leading '"course files/' from folder 'path'
    """
    return long_folder_name[13:]
