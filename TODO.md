## Changes since version 0.1:
* new commands
  * add_module
  * list_modules
* when creating a new page or module, refuse when page already exist
* when adding an item to a module, refuse when it already present
* added --force
* added --create
* added --publish
* can now also files to a module
* some code reorganisation and refactoring

## TO DO
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
  - document well the file url (https://canvas.instance.com/courses/12345/files/folder/subfolder/file.ext, this is not an existing url...)
  - open for other file urls (https://canvas.instance.com/courses/12345/files/67890/download?download_frd=1, https://canvas.instance.com/courses/12345/files/folder/subfolder?preview=67890, others?)
* consider adding commands to delete pages, files and folders, and remove items from modules
* consider adding commands to post announcements
  - https://canvasapi.readthedocs.io/en/stable/discussion-topic-ref.html
  - https://canvas.instructure.com/doc/api/discussion_topics.html
* add more tests
* use Free Canvas Course for a test instance that anyone can run tests against?
  - https://www.instructure.com/canvas/try-canvas
* turn into a Python package
* get a doi
* FIXME in add_to_module
* bug: running `canvasCourseCli add_to_module -u https://instance.instructure.com/courses/9999/pages/name-of-page -t '' --create` gives long traceback ending with `canvasapi.exceptions.BadRequest: {"message":"missing module name"}`
* reduce code redundancy for argparse
  - maybe use `-- parent`? https://docs.python.org/3/library/argparse.html#parents
* in `add_page.py`: replace `published` with `args.publish`:
```
published = 'false'
if args.publish:
    published = 'true'
```
* catch this error that occurs when the Canvas room is locked for modifications:
```
File "/Users/alexajo/github/canvasCourseCli/canvasCourseCli", line 74, in main
  AllCommands()
File "/Users/alexajo/github/canvasCourseCli/canvasCourseCli", line 70, in __init__
  cmd(sys.argv[2:])
File "/Users/alexajo/github/canvasCourseCli/add_file.py", line 49, in main
  result = folder.upload(args.file_to_send)
File "/Users/alexajo/anaconda3/envs/doconce_develop/lib/python3.9/site-packages/canvasapi/folder.py", line 136, in upload
  ...
canvasapi.exceptions.Unauthorized: [{'message': 'brukeren er ikke autorisert til å utføre den handlingen'}]
```

## Things I will not develop
