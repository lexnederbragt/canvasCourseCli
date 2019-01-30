canvastf
--------

Python tools for adding, retrieving and updating content on a Canvas instance. Work in progress.

Depends on [canvasAPI](https://canvasapi.readthedocs.io/en/latest/).

## Configuration file
Requires a configuration file with a [Canvas API key](https://community.canvaslms.com/docs/DOC-14409-4214861717). Default config file is `~/.config/canvasapi.conf`, but this can be changed when calling the tool.

The config file should have this structure with at least one base url and corresponding API key:

```
[base_url]
api_key = YOURKEY

[base_url2]
api_key = YOURKEY2
```

## The name
`canvastf` stands for "Canvas To From".
