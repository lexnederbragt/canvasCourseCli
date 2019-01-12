#canvas_instance = 'uio'
#course_code = 'bios1100'
#html_to_send = 'api_test.html'
# url_for_page = 'testing-canvas-api'

# optional
config_file = '~/.config/canvasapi.conf' # default


import argparse
# help text and argument parser
desc = '\n'.join(["To be added.",
                 "Add note about default config file '~/.config/canvasapi.conf'"
                 "An optional argument -c/--config_file can be used with the path to the config file."
                  ])
parser = argparse.ArgumentParser(description=desc)
parser.add_argument("instance", help="The name of the Canvas instance as defined in the config file")
parser.add_argument("url", help="The last part of the url of the page to de updated, the part following '/pages/'")
parser.add_argument("html_file", help="The name of the html file that will be sent to Canvas")
parser.add_argument("-c", "--config_file", help="Path to config file")
parser.add_argument("-s", "--show_config", help="Show the content of the config file", action="store_true")
args = parser.parse_args()
print(args)
