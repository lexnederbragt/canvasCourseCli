import sys
import argparse
from api import get_course, split_page_url

def parse_args(args):
    # help text and argument parser
    # solution based on https://stackoverflow.com/a/24181138/462692
    desc = '\n'.join(["Updates an existing page on canvas with the content of an html file.",
                     "An optional argument -c/--config_file can be used with the path to the config file. "
                     "Otherwise the default config file '~/.config/canvasapi.conf' will be used.\n"
                      ])
    parser = argparse.ArgumentParser(description=desc)
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument("-u", "--url", help="The full url of the page to be updated", required = True)
    required_named.add_argument("-f", "--html_file", help="The path to the html file that will be sent to Canvas", required = True)
    parser.add_argument("-cf", "--config_file", help="Path to config file", default = '~/.config/canvasapi.conf')
    args = parser.parse_args(args)
    return args

def main(args):
    args = parse_args(args)

    API_URL, course_id, page_name = split_page_url(args.url)
    course =  get_course(API_URL, course_id, args.config_file)

    # read new content
    with open(args.html_file, 'r') as html_file:
        html_content = html_file.read()#.replace('\n', '')

    # get the course page
    try:
        page_to_update = course.get_page(page_name)
    except:
        sys.exit("Error: could not find page '%s' on Canvas for updating.\nFull url: %s" % (page_name, args.url))

    # Get current revision
    old_rev = page_to_update.get_revisions()[0]

    # update the course page
    api_call_result = page_to_update.edit(wiki_page = {"title":page_to_update.title, "body":html_content})

    # testing whether the update has happened
    # in which case the revision has changed
    new_rev = page_to_update.get_revisions()[0]
    if str(new_rev) != str(old_rev):
        print("Sucessfully updated page "+ args.url + " to revision '" + str(new_rev) + "'")
    else:
        print("The API call was succesful, but the page %s appears not to have recieved a new revision number." % args.url)
        print("This could mean the current content is identical to the html file provided.")

if __name__ == "__main__":
    main(sys.argv[1:])
