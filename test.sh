# testing script on UiO canvas instance
python canvastf.py send_html -u https://uio.instructure.com/courses/5848/pages/testing-canvas-api -f api_test.html
python canvastf.py view_html -u https://uio.instructure.com/courses/5848/pages/testing-canvas-api
python create_folder.py -u https://uio.instructure.com/courses/4258/files/folder/test
