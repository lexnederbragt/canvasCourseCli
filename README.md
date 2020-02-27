cvupdate
--------

A Python-based command-line tool for adding, retrieving and updating content on a Canvas instance.

 * [Dependencies](#Dependencies)
 * [Configuration file](#configuration-file)
 * [Basic usage](#basic-usage)
    * [Examples](#examples)
 * [The name](#the-name)
 * [Why I developed this](#why-i-developed-this)

## Dependencies

Depends on [canvasAPI](https://canvasapi.readthedocs.io/en/latest/).

## Configuration file
Requires a configuration file with a [Canvas API key](https://community.canvaslms.com/docs/DOC-14409-4214861717). Default config file is `~/.config/canvasapi.conf`, but this can be changed when calling the tool.

The config file should have this structure with at least one base url (something like https://instance.instructure.com) and corresponding API key:

```
[base_url]
api_key = YOURKEY

[base_url2]
api_key = YOURKEY2
```

## Basic usage

```
usage: cvupdate.py <command> [<args>]

Available:

add_page      -u URL -t TITLE -f HTML_FILE  Add a new page to Canvas.
update_page   -u URL -f HTML_FILE           Update the content of a page on Canvas.
view_page     -u URL                        View the content of a page on Canvas.
tree          -u URL                        List all folders for a course on Canvas.
list_files    -u URL                        List all files for a course on Canvas.
list_pages    -u URL                        List all pages for a course on Canvas.
dump          -u URL                        Download all files and pages for a course on Canvas.
create_folder -u URL                        Create a new folder on Canvas.
add_file      -u URL -f FILE_TO_SEND        Add a file to a folder on Canvas.
add_to_module -u URL -m MODULE_NAME         Add a page on Canvas to a module.

```

### Examples
To add a new page to canvas (based on a file in html format):

```
cvupdate.py add_page -u https://instance.instructure.com/courses/9999 -t 'My new page' -f file.html
```
NOTE the url of the new page becomes `https://instance.instructure.com/courses/9999/pages/my-new-page`

To view the content of a page on canvas (in html format):

```
cvupdate.py view_page -u https://instance.instructure.com/courses/9999/pages/name-of-page
```

To replace the content of an existing page with content of a file (in html format):
```
cvupdate.py update_page -u https://instance.instructure.com/courses/9999/pages/name-of-page -f file.html
```

To create a new folder:
```
cvupdate.py create_folder -u https://instance.instructure.com/courses/9999/files/folder/name-of-folder
```

To add a new file, or overwite an existing one with the same name:
```
cvupdate.py add_file -u https://instance.instructure.com/courses/9999/files/folder/name-of-folder/name-of-file -f name-of-file.pdf
```

To add an existing page to an existing module:
```
cvupdate.py add_to_module -u https://instance.instructure.com/courses/9999/pages/name-of-page -n 'Name of module'
```

## The name
`cvupdate` stands for "canvas update".

## Why I developed this
I wanted to be able to use the command line to view, add and update content on Canvas. For example:
* write pages for Canvas in Markdown, put these under version control, and use a Makefile to automatically convert them to html (using pandoc) and add or update them on the course's Canvas instance
* send files to Canvas from the command line
* add pages to modules
