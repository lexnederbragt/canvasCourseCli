# steps before testing:
# change api_test.html
# delete folder https://uio.instructure.com/courses/4258/test

URL=https://uio.instructure.com/courses/4258
# testing script on UiO canvas instance
cvupdate.py update_page -u ${URL}/pages/testing-canvas-api -f api_test.html
echo
cvupdate.py view_page -u ${URL}/pages/testing-canvas-api
echo
cvupdate.py create_folder -u ${URL}/files/folder/test
echo
cvupdate.py add_file -u ${URL}/files/folder/test -f test.sh
