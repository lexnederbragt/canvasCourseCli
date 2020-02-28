# use as - replacing url with one you have API access to:
#
# sh test.sh https://instance.instructure.com/courses/9999


# preparational steps before testing:
# have a page called ${URL}/pages/testing-canvas-api
# remove any pages whose name is or start with ${URL}/pages/adding-a-page
# change api_test.html (optional)
# delete folder ${URL}/test

URL=$1

if [ -z "$URL" ]
then
      echo "use as:    test.sh URL"
else

    echo Updating ${URL}/pages/testing-canvas-api
    cvupdate.py update_page -u ${URL}/pages/testing-canvas-api -f api_test.html
    echo
    echo Viewing ${URL}/pages/testing-canvas-api
    cvupdate.py view_page -u ${URL}/pages/testing-canvas-api
    echo
    echo Creating ${URL}/files/folder/test
    cvupdate.py create_folder -u ${URL}/files/folder/test
    echo
    echo Adding file api_test.txt to ${URL}/files/folder/test
    cvupdate.py add_file -u ${URL}/files/folder/test -f api_test.txt
    echo
    echo Adding and publishing page "Adding a page" from file api_test2.html
    cvupdate.py add_page -u ${URL} -t "Adding a page" -f api_test2.html -p
    echo
    echo Adding ${URL}/pages/adding-a-page to module 'API test module'
    cvupdate.py add_to_module -u ${URL}/pages/adding-a-page -m 'API test module'
    echo
    echo Listing all pages
    cvupdate.py list_pages -u ${URL}
    echo
    echo Listing all files
    cvupdate.py list_files -u ${URL}
fi
