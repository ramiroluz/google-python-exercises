#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

# Problem description:
# https://developers.google.com/edu/python/exercises/copy-special


import sys
import re
import os
import shutil
import subprocess
import shlex

"""Copy Special exercise

"""


# +++your code here+++
# Write functions and modify main() to call them
def get_special_paths(src_dir):
    all_files = os.listdir(src_dir)
    fname_expression = re.compile('^.*__\w.*__.*')
    return [
        os.path.abspath(fname) for fname in all_files
        if fname_expression.match(fname)
    ]


def copy_to(paths, dst_dir):
    os.path.isdir(dst_dir) or os.makedirs(dst_dir)

    for fname in paths:
        shutil.copy(fname, dst_dir)


def zip_to(paths, zippath):
    command = 'zip -j {} {}'.format(zippath, ' '.join(paths))
    print("Command I'm going to do: {}".format(command))
    try:
        subprocess.call(shlex.split(command))
    except OSError as e:
        print('zip I/O error: {}'.format(e.strerror))
        print('zip error: Could not create output file ({})'.format(zippath))


def main():
    # This basic command line argument parsing code is provided.
    # Add code to call your functions below.

    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]
    if not args:
        print("usage: [--todir dir][--tozip zipfile] dir [dir ...]")
        sys.exit(1)

    # todir and tozip are either set from command line
    # or left as the empty string.
    # The args array is left just containing the dirs.
    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    tozip = ''
    if args[0] == '--tozip':
        tozip = args[1]
        del args[0:2]

    if len(args) == 0:
        print("error: must specify one or more dirs")
        sys.exit(1)

    # +++your code here+++
    # Call your functions
    paths = []
    for src_dir in args:
        paths.extend(get_special_paths(src_dir))

    if todir:
        copy_to(paths, todir)

    if tozip:
        zip_to(paths, tozip)


if __name__ == "__main__":
    main()
