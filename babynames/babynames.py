#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re

"""Baby Names exercise

Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 -Extract the year and print it
 -Extract the names and rank numbers and just print them
 -Get the names data into a dict and print it
 -Build the [year, 'name rank', ... ] list and print it
 -Fix main() to use the extract_names list
"""


def extract_names(filename):
    """
    Given a file name for baby.html, returns a list starting with the year string
    followed by the name-rank strings in alphabetical order.
    ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
    """
    # +++your code here+++
    return


def test_extract_year():
    html_text = (
        '<html>\n'
        '  <body>\n'
        '    <h3 align="center">Popularity in 1990</h3>\n'
        '  </body>\n'
        '</html>'
    )
    expected = '1990'
    the_year = extract_year(html_text)
    assert expected == the_year


def extract_year(html_text):
    comp = re.compile(
        '(?:<h3 align="center">Popularity in )'  # <h3>
        '(\d{4}?)'  # year
        '(?:</h3>)'  # </h3>
    )
    year = comp.findall(html_text)
    if year:
        return year[0]
    return ''


def test_extract_rows():
    html_text = (
        '<html>\n'
        '  <body>\n'
        '    <h3 align="center">Popularity in 1990</h3>\n'
        '      <table>\n'
        '        <tr align="right">\n'
        '          <td>1</td><td>Michael</td><td>Jessica</td>\n'
        '        </tr>\n'
        '        <tr align="right">\n'
        '          <td>2</td><td>Christopher</td><td>Ashley</td>\n'
        '        </tr>\n'
        '        <tr align="right">\n'
        '          <td>3</td><td>Matthew</td><td>Brittany</td>\n'
        '        </tr>\n'
        '  </body>\n'
        '</html>'
    )
    expected = [
        '<td>1</td><td>Michael</td><td>Jessica</td>',
        '<td>2</td><td>Christopher</td><td>Ashley</td>',
        '<td>3</td><td>Matthew</td><td>Brittany</td>',
    ]

    rows = extract_rows(html_text)
    assert expected == rows


def extract_rows(html_text):
    comp = re.compile('(<td>.*</td>)')
    rows = comp.findall(html_text)
    return rows or []


def tests():
    test_extract_year()
    test_extract_rows()


def test_extract_cols():
    rows = [
        '<td>1</td><td>Michael</td><td>Jessica</td>',
        '<td>2</td><td>Christopher</td><td>Ashley</td>',
        '<td>3</td><td>Matthew</td><td>Brittany</td>',
    ]

    expected = [
        ('1', 'Michael', 'Jessica'),
        ('2', 'Christopher', 'Ashley'),
        ('3', 'Matthew', 'Brittany')
    ]

    cols = extract_cols(rows)
    assert expected == cols


def extract_cols(rows):
    comp = re.compile(
        '(?:<td>)'  # <td>
        '(.*?)'  # row data
        '(?:</td>)'  # </td>
    )
    cols = comp.findall(html_text)
    return tuple(cols) or tuple()


def test_cols_to_dict():
    cols = [
        ('1', 'Michael', 'Jessica'),
        ('2', 'Christopher', 'Ashley'),
        ('3', 'Matthew', 'Brittany')
    ]

    expect = {
        '1': ('Michael', 'Jessica'),
        '2': ('Christopher', 'Ashley'),
        '3': ('Matthew', 'Brittany'),
    }

    data = cols_to_dict(cols)
    assert expected == data


def cols_to_data(cols):
    pass


def main():
    # This command-line parsing code is provided.
    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]

    if not args:
        print('usage: [--summaryfile] file [file ...]')
        sys.exit(1)

    # Notice the summary flag and remove it from args if it is present.
    summary = False
    if args[0] == '--summaryfile':
        summary = True
        del args[0]

    tests()
        # +++your code here+++
        # For each filename, get the names, then either print the text output
        # or write it to a summary file


if __name__ == '__main__':
    main()
