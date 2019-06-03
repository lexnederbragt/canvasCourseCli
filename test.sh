URL=https://uio.instructure.com/courses/4258/
# testing script on UiO canvas instance
python cvupdate.py update_html -u ${URL}pages/testing-canvas-api -f api_test.html
echo
python cvupdate.py view_html -u ${URL}pages/testing-canvas-api
echo
python cvupdate.py create_folder -u ${URL}files/folder/test
echo
python cvupdate.py add_file -u ${URL}files/folder/test -f test.sh
