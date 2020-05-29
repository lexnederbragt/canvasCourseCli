import sys
import argparse
from api import get_course, split_url, page_exists
from add_page import create_page

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
    parser.add_argument("--create", help="If the page does not exist yet, \
    add; requires -t/--title (default: off, and warn instead)", action='store_true')
    parser.add_argument("-t", "--title", help="The title the page, enclosed in quotation marks if it \
    contains one or more spaces. Needed when the page is also to be added. Note that the url of the page will be the title in lower case, with each space replaced by a dash", required = False)
    parser.add_argument("-p", "--publish", help="Publish the page on Canvas at the time of creation (default: leave unpublished)", action='store_true')
    parser.add_argument("-cf", "--config_file", help="Path to config file", default = '~/.config/canvasapi.conf')
    args = parser.parse_args(args)
    return args

def main(args):
    args = parse_args(args)

    # extract course information from url and get course
    API_URL, course_id, page_name = split_url(args.url, expected = 'page')
    course =  get_course(API_URL, course_id, args.config_file)

    # read new content
    with open(args.html_file, 'r') as html_file:
        html_content = html_file.read()#.replace('\n', '')

    # test whether page exists
    if page_exists(course, page_name):
        # page does exist
        page_to_update = course.get_page(page_name)
        # Get current revision
        old_rev = page_to_update.get_revisions()[0]

        # update the course page
        api_call_result = page_to_update.edit(wiki_page = {
            "title":page_to_update.title,
            "body":html_content
            })

        # testing whether the update has happened
        # in which case the revision has changed
        new_rev = page_to_update.get_revisions()[0]
        if str(new_rev) != str(old_rev):
            print("Successfully updated page "+ args.url + " to revision '" + str(new_rev) + "'")
        else:
            print("The API call was succesful, but the page %s appears not to have recieved a new revision number." % args.url)
            print("This could mean the current content is identical to the html file provided.")
    else:
        # page does not exist
        message =f"Could not find page '{page_name}' on Canvas for updating.\n"
        if args.create:
            # check that title is given
            if not args.title:
                message += "Could not create page as title is missing.\n"
                message += "Use -t/--title to in addition to --create to create the page."
                sys.exit(message)
            message += "Will attempt to create the page."
            print(message)
            new_page = create_page(course, args.title, html_content, args.publish)
            message = "Sucessfully added page '%s'.\nFull url: '%s'." \
            %(new_page.title, API_URL + '/courses/' + course_id + '/pages/' + new_page.url)
            print(message)
        else:
            message = "Error: " + message
            message += f"Full url: '{args.url}'\n"
            message += "Use --create to create the page before adding the file.\n"
            message += "Note that this requires the use of -t/--title."
            sys.exit(message)


if __name__ == "__main__":
    main(sys.argv[1:])
