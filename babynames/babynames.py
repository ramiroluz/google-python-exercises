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

def test_reader(filename):
    try:
            from StringIO import StringIO
    except ImportError:
            from io import StringIO

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

    return StringIO(html_text)


def test_extract_names():
    expected = [
        '1990',
        'Ashley 2',
        'Brittany 3',
        'Christopher 2',
        'Jessica 1',
        'Matthew 3',
        'Michael 1',
    ]

    names = extract_names('babies.html', reader=test_reader)
    assert names == expected

def extract_names(filename, reader=open):
    """
    Given a file name for baby.html, returns a list starting with the year string
    followed by the name-rank strings in alphabetical order.
    ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
    """
    try:
        babies = reader(filename)
        html_text = babies.read()
    finally:
        babies.close()

    year = extract_year(html_text)
    rows = extract_rows(html_text)
    cols = extract_cols(rows)
    data = cols_to_dict(cols)

    baby_names = []
    for rank, names in data.items():
        for name in names:
            baby_names.append('{} {}'.format(name, rank))

    return [year] + sorted(baby_names)


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
    cols = [
        tuple(comp.findall(row)) for row in rows
    ]
    return cols


def test_cols_to_dict():
    cols = [
        ('1', 'Michael', 'Jessica'),
        ('2', 'Christopher', 'Ashley'),
        ('3', 'Matthew', 'Brittany')
    ]

    expected = {
        '1': ('Michael', 'Jessica'),
        '2': ('Christopher', 'Ashley'),
        '3': ('Matthew', 'Brittany'),
    }

    data = cols_to_dict(cols)
    assert expected == data


def cols_to_dict(cols):
    return {item[0] : (item[1], item[2]) for item in cols}


def tests():
    test_extract_year()
    test_extract_rows()
    test_extract_cols()
    test_cols_to_dict()
    test_extract_names()


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
        symmary_filename = args[1]
        del args[0]
        del args[1]

    # +++your code here+++
    # For each filename, get the names, then either print the text output
    # or write it to a summary file
    for filename in args:
        babies_list = extract_names(filename)
        if summary:
            with open(summary_filename, 'a') as summary_file:
                summary_file.write('\n'.join(babies_list))
        else:
            print('\n'.join(babies_list))

    # tests()


if __name__ == '__main__':
    main()
