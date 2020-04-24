# TO DO
* enable use of shortname for a course instead of full url
* enable sending a file to the root folder
* enable modifying the course homepage
* instead of using the full base url, use the part following `http{s}://`
* capture urls with double forward slashes `//`
* implement creating a new folder in a new folder in one operation
* when creating a new page, enable option to add to an existing module in the same operation
* when creating a new page, check whether page already exists
* enable adding any item using add_to_module (add_to_module can figure out file versus folder and adjust accordingly)
* improve handling of exceptions (the current `try - except` solution is probably not good practice)
* add flag for `dump.py` to only download pages or only files
* add flag for `dump.py` to do a dry run
* consider adding commands to delete pages, files and folders, and remove items from modules
* add more tests
* turn into a Python package
* get a doi

## Things I will not develop
* when updating a page, check whether page already exists and if not, enable in the same operation
  - complicated as then the user needs to provide a title and optionally use the -p option to publish the page at the same time.
