# steps before testing:
# remove page(s) https://uio.instructure.com/courses/4258/pages/adding-a-page
# change api_test.html (optional)
# delete folder https://uio.instructure.com/courses/4258/test

URL=https://uio.instructure.com/courses/4258
# testing script on UiO canvas instance
echo Updating ${URL}/pages/testing-canvas-api
cvupdate.py update_page -u ${URL}/pages/testing-canvas-api -f api_test.html
echo
echo viewing ${URL}/pages/testing-canvas-api
cvupdate.py view_page -u ${URL}/pages/testing-canvas-api
echo
echo creating ${URL}/files/folder/test
cvupdate.py create_folder -u ${URL}/files/folder/test
echo
echo adding file api_test.txt to ${URL}/files/folder/test
cvupdate.py add_file -u ${URL}/files/folder/test -f api_test.txt
echo
echo adding page "Adding a page" from file api_test2.html
cvupdate.py add_page -u ${URL} -t "Adding a page" -f api_test2.html
echo
echo Adding ${URL}/pages/adding-a-page to module 'API test module'
cvupdate.py add_to_module -u ${URL}/pages/adding-a-page -m 'API test module'
