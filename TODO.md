# TO DO
* enable use of shortname for a course instead of full url
* enable sending a file to the root folder
* enable modifying the course homepage
* instead of using the full base url, use the part following `http{s}://`
* capture urls with double forward slashes `//`
* implement creating a new folder in a new folder in one operation
* improve handling of exceptions (the current `try - except` solution is probably not good practice)
* add flag for `dump.py` to only download pages or only files
* add flag for `dump.py` to do a dry run
* add_module
  - enable publishing module
  - enable checking whether module of same name already exists, do not add unless `--force`
  - enable adding any item (add_to_module can figure out file versus folder and adjust accordingly)
* consider adding commands to delete pages, files and folders, and remove items from modules
* add more tests
* turn into a Python package
* get a doi
* reduce code redundancy for argparse
  - maybe use `-- parent`? https://docs.python.org/3/library/argparse.html#parents
* in `add_page.py`: replace `published` with `args.publish`:
```
published = 'false'
if args.publish:
    published = 'true'
```

## Things I will not develop
