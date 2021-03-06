canvasCourseCli
--------

A Python-based command-line tool for retrieving, adding and updating
content, pages, files and modules exposed to students and teachers,
for a Canvas instance (course).

Not to be confused with the [Canvas Data CLI Tool](https://community.canvaslms.com/docs/DOC-6600-how-to-use-the-canvas-data-cli-tool#jive_content_id_Overview), which can by used to extract course data from the database.

 * [Dependencies](#Dependencies)
 * [Configuration file](#configuration-file)
 * [Basic usage](#basic-usage)
 * [Examples](#examples)
 * [About page titles and urls](#about-page-titles-and-urls)
 * [Testing the tool](#testing-the-tool)
 * [The name](#the-name)
 * [Why I developed this](#why-i-developed-this)

## Dependencies

Depends on
* [canvasAPI](https://canvasapi.readthedocs.io/en/latest/)
* [pathlib](https://pypi.org/project/pathlib/)
* optional: [pytest](https://docs.pytest.org/en/latest/) for tests

## Configuration file

Requires a configuration file with a [Canvas API key](https://community.canvaslms.com/docs/DOC-14409-4214861717). The default config file is `~/.config/canvasapi.conf`, but this can be changed when calling the tool.

The config file should have this structure with at least one pair of
* a base url, enclosed in square brackets, similar to `[https://instance.instructure.com]`
* the corresponding API key, something like `api_key = rpLoM9Yc62Qzv$JLswq4E#70....M1q&$B9hSFPA`


```
[base_url]
api_key = YOURKEY

[base_url2]
api_key = YOURKEY2
```

## Basic usage

```
usage: canvasCourseCli <command> [<args>]

Available:

    list_files    -u URL                        List all files for a course on Canvas.
    list_pages    -u URL                        List all pages for a course on Canvas.
    tree          -u URL                        List all folders for a course on Canvas.
    dump          -u URL                        Download all files and pages for a course on Canvas.
    view_page     -u URL                        View the content of a page on Canvas.
    add_page      -u URL -t TITLE -f HTML_FILE  Add a new page to Canvas.
    create_folder -u URL                        Create a new folder on Canvas.
    add_file      -u URL -f FILE_TO_SEND        Add a file to a folder on Canvas.
    update_page   -u URL -f HTML_FILE           Update the content of a page on Canvas.
    add_module    -u URL -m MODULE_NAME         Add a new module to a course on Canvas.
    list_modules  -u URL                        List all modules for a course on Canvas.
    add_to_module -u URL -m MODULE_NAME         Add a page on Canvas to a module.
```

### General aspects

* `canvasCourseCli` is _restrictive_:
  - when an item to be added is already in place,
    `canvasCourseCli` will throw an error
  - when an item to is to be added to a non-existing folder or module,
    or a non-existing page is to be updated,
    `canvasCourseCli` will throw an error
* `canvasCourseCli` is also _permissive_:
  - using the `-f/--force` flag will add modules or pages already present another time,
    or add an item that is already added to a module another time
  - using the `-c/--create` flag will create missing modules or folders
    that items are to be added too, or missing pages to be updated
* added items can optionally be published using the `-p/--publish` flag

### Examples

To view the content of a page on canvas (in html format):

```
canvasCourseCli view_page -u https://instance.instructure.com/courses/9999/pages/name-of-page
```

To add a new page to canvas (based on a file in html format):

```
canvasCourseCli add_page -u https://instance.instructure.com/courses/9999 -t 'My new page' -f file.html
```
NOTE the url of the new page becomes `https://instance.instructure.com/courses/9999/pages/my-new-page`

To replace the content of an existing page with content of a file (in html format):
```
canvasCourseCli update_page -u https://instance.instructure.com/courses/9999/pages/name-of-page -f file.html
```

To replace the content of a page with content of a file (in html format),
optionally creating the page if it is not yet present (this requires the title of the page):
```
canvasCourseCli update_page -u https://instance.instructure.com/courses/9999/pages/name-of-page -f file.html --create --title="Name of page"
```

To create a new folder:
```
canvasCourseCli create_folder -u https://instance.instructure.com/courses/9999/files/folder/name-of-folder
```

To add a new file, or overwrite an existing one with the same name
- note that overwriting a file changes its URL:
```
canvasCourseCli add_file -u https://instance.instructure.com/courses/9999/files/folder/name-of-folder/name-of-file -f name-of-file.pdf
```

To add an existing page to an existing module:
```
canvasCourseCli add_to_module -u https://instance.instructure.com/courses/9999/pages/name-of-page -t 'Name of module'
```

To add an existing page to a module, optionally creating the module if it is not yet present:
```
canvasCourseCli add_to_module -u https://instance.instructure.com/courses/9999/pages/name-of-page -t 'Name of module' --create"
```

## About page titles and urls

If a page added to Canvas has the title "This is the title",
the url of the page becomes https://instance.instructure.com/courses/9999/pages/this-is-the-title, i.e., in lower case and spaces replaced with dashes.
Take care to advised to match the url for a page with it's title when creating a new page.
Also be careful with non standard characters (such as æ, ø, å).

## Testing the tool

If you have a Canvas course instance you don't mind using, executing the shell script `test.sh` runs a few commands to test
- viewing, updating, and adding a page
- create a folder and add a file to it
- list all pages and files

## The name

`canvasCourseCli` is inspired by `canvasDataCli`, the command name of the [Canvas Data CLI Tool](https://community.canvaslms.com/docs/DOC-6600-how-to-use-the-canvas-data-cli-tool#jive_content_id_Overview).

## Why I developed this

I wanted to be able to use the command line to view, add and update content on Canvas. For example:
* write pages for Canvas in Markdown, put these under version control, and use a Makefile to automatically convert them to html (using [pandoc](https://pandoc.org)) and add or update them on the course's Canvas instance
* send files to Canvas from the command line
* add pages to modules from the command line
