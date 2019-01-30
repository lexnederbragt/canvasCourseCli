import sys
import argparse
from api import get_course, split_url

def parse_args(args):
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
    args = parser.parse_args(args)
    return args

def main(args):
    args = parse_args(args)

    page_name = split_url(args.url)[2]
    course =  get_course(args.url, args.config_file)

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

if __name__ == "__main__":
    main(sys.argv[1:])
