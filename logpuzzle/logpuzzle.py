#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def test_reader(filename):
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO

    log_text = (
        '10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET '
        '/~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" '
        '"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; '
        'rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"'
    )

    return StringIO(log_text)


def test_read_urls():
    expected = [
        'http://foo.com/~foo/puzzle-bar-aaab.jpg',
    ]

    urls = read_urls('animals_foo.com', reader=test_reader)

    assert urls == expected


def read_urls(filename, reader=open):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    # +++your code here+++
    log_text = reader(filename).read()
    resource_regex = re.compile('(?:GET )(.*puzzle.*)(?: HTTP)')
    resources = resource_regex.findall(log_text)
    hostname = filename.split('_')[-1]
    return ['http://{}{}'.format(hostname, resource) for resource in sorted(resources)] 


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    
    tag_template = '<img src="{}">'

    index_template = (
        '<html>\n'
        '  <body>\n'
        '    {}'
        '  </body>\n'
        '</html>\n'
    )

    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)

    paragraphs = []
    for idx, img_url in enumerate(img_urls):
        extension = os.path.splitext(img_url)[-1]
        filename = 'img{}{}'.format(idx, extension)
        paragraphs.append(tag_template.format(filename))
        urllib.urlretrieve(img_url, os.path.join(dest_dir, filename))

    index_text = index_template.format(''.join(paragraphs))
    with open(os.path.join(dest_dir, 'index.html'), 'w') as index:
        index.write(index_text)


def tests():
    test_read_urls()


def main():
    args = sys.argv[1:]

    if not args:
        print('usage: [--todir dir] logfile ')
        sys.exit(1)

    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    img_urls = read_urls(args[0])

    if todir:
        download_images(img_urls, todir)
    else:
        print('\n'.join(img_urls))

    # tests()

if __name__ == '__main__':
    main()
