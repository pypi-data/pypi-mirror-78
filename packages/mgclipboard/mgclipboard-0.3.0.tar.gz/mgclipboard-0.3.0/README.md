MgClipboard
============

Clipboard middleware for [Papermerge DMS](https://github.com/ciur/papermerge).
Designed as Django reusable app.

## Installation

Install it using pip::
    
    pip install mgclipboard

Add app to INSTALLED_APPS in settings.py:

    INSTALLED_APP = (
    ...
    'mgclipboard',
    ...
    )

Add it to MIDDLEWARE list:

    MIDDLEWARE = [
        ...
        # AFTER
        # * django.contrib.sessions.middleware
        # * django.contrib.auth.middleware
        'mgclipboard.middleware.ClipboardMiddleware'
        ...
    ]

mgclipboard.middleware is dependent on django.contrib.sessions and django.contrib.auth middleware. Thus, dependencies must be included first in MIDDLEWARE list.

## Usage

MgClipboard middleware adds 3 attributes to the request object:

* request.clipboard
* request.nodes (shortcut for request.clipboard.nodes)
* request.pages (shortcut for request.clipboard.pages)

To add list of node ids to clipboard use:

    request.nodes.add(['id1', 'id2', ...])

To retrieve all node ids (folder or documents) currently in the clipboard call:

    request.nodes.all()

To clear all nodes data from the clipboard:

    request.nodes.clear()

To add pages, all belonging to same document, use:
        
    request.pages.add(
        doc_id=doc_id,
        page_nums=[1, 2, 3]
    )

Important! page_nums is a list of page numbers within document doc_id. Page numbering starts with 1.


All pages currently in clipboard are returned by:

    request.pages.all()

To clear all pages data from the clipboard:

    request.pages.clear()