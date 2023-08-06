"""Utilities related to console applications


Copyright 2015 Heung Ming Tai

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys

import six

import threading
from sorno import mathlib


def input(prompt, file=None):
    """
    Just like raw_input in python2 or input in python3, but can optionally
    redirect the prompt to other file objects.
    Args:
        prompt: A string for the prompt.
        file: Optional. A file object to the prompt is written to.
    """
    if file is None:
        return six.moves.input(prompt)
    else:
        old_stdout = sys.stdout
        try:
            sys.stdout = file
            return six.moves.input(prompt)
        finally:
            sys.stdout = old_stdout


def pick_items(items):
    for i, item in enumerate(items, 1):
        print("%d)" % i, item, file=sys.stderr)

    reply = input("Please choose:", file=sys.stderr)

    intervals = parse_intervals(reply)

    nums = []
    for interval in intervals:
        nums.extend(range(interval.start, interval.end + 1))

    chosens = [items[num - 1] for num in nums]
    return chosens


def num_str_to_nums(num_str):
    if num_str:
        if '-' in num_str:
            start, end = num_str.split('-')
            return list(range(int(start), int(end) + 1))
        else:
            return [int(num_str)]
    else:
        return []


class DataPrinter(object):
    PRINT_STYLE_HTML_TABLE = 'html'
    PRINT_STYLE_PLAIN = 'plain'
    PRINT_STYLE_R = 'R'
    PRINT_STYLE_TABLE = 'table'
    PRINT_STYLE_VERBOSE = 'verbose'
    NICETABLE_COL_LEN = 80
    PRINT_STYLE_R = 'R'
    PRINT_STYLE_NICETABLE = 'nicetable'
    PRINT_STYLE_STREAMING_PLAIN = 'streaming-plan'

    OPTION_TITLE = 'title'
    OPTION_ADDITIONAL_TRAILING_CONTENT = 'additional-trailing-content'

    def __init__(
        self,
        data,
        headers=(),
        header_types=None,
        delimiter='\t',
        max_col_len=NICETABLE_COL_LEN,
        print_func=print,
        streaming=False,
    ):
        """Constructs a DataPrinter object

        Args:
          data: A list of dict's or a list of lists. Each dict or list
              represents a row of data. If it's a dict, the keys are the
              column names in strings and the values are the column values in
              strings.  If it's a list, then each item is the value of a
              column of the row. Each value should be a string properly
              formatted, since DataPrinter does not do any special formatting
              of each value.

              If streaming is True, data should be a Queue with
              the sentinel value None.

          headers: Optionally supply a list of headers in strings to control
              what columns are printed out and what order are the columns
              printed.

          header_types: A list of strings representing the types of the
              headers. It's currently used for PRINT_STYLE_R form. This is not
              needed if you are not using PRINT_STYLE_R.

          delimiter: The delimiter in string for separating column values. By
              default it's a tab character.

          max_col_len: An integer to indicate the maximum column length when
              the data is printed in PRINT_STYLE_NICETABLE. By default it's
              80.

          print_func: A function that takes a string as an argument. The
              function is used for printing the data. By default it uses the
              built-in print function.

          streaming: The data will come as a stream. This should
              be used if PRINT_STYLE_STREAMING_PLAIN is used for
              printing result.
        """
        if streaming:
            self.data = iter(data.get, None)
        else:
            if not hasattr(data, "__getitem__"):
                data = list(data)

            if not headers and data and isinstance(data[0], dict):
                # infer headers from data
                headers = sorted(data[0].keys())

            if data and isinstance(data[0], dict):
                self.data = self._convert_list_of_dicts(headers, data)
            else:
                self.data = data

        self.headers = headers
        self.header_types = header_types
        self.delimiter = delimiter
        self.max_col_len = max_col_len
        self.print_func = print_func

    def _convert_list_of_dicts(self, headers, ls_of_dicts):
        """
        Convert list of dicts to list of lists.
        """
        data = [[d[header] for header in headers] for d in ls_of_dicts]
        return data

    def print_result(self, style=PRINT_STYLE_TABLE, options=None):
        if options is None:
            options = {}

        if style == DataPrinter.PRINT_STYLE_R:
            json_headers = []
            for header, t in zip(self.headers, self.header_types):
                h = {'name': header, 'type': t}
                json_headers.append(
                    json.dumps(h).replace('\t', '').replace('\n', '')
                    )
            self.print_func(self.delimiter.join(json_headers))
            self.print_data()
        elif style == DataPrinter.PRINT_STYLE_PLAIN:
            self.print_data()
        elif style == DataPrinter.PRINT_STYLE_STREAMING_PLAIN:
            self.print_data_streaming()
        elif style == DataPrinter.PRINT_STYLE_VERBOSE:
            self.print_verbose()
        elif style == DataPrinter.PRINT_STYLE_HTML_TABLE:
            self.print_html_table(options)
        elif style == DataPrinter.PRINT_STYLE_NICETABLE:
            self.print_table(is_nicetable=True)
        else:
            self.print_table()

    def print_data_streaming(self):
        threading.Thread(target=self.print_data).start()

    def print_data(self):
        # Each value is a row with ^A as delimiter
        for row in self.data:
            self.print_func(self.delimiter.join(row))

    def print_table(self, is_nicetable=False):
        max_widths = [len(header) for header in self.headers]
        for row in self.data:
            for i, col in enumerate(row):
                max_widths[i] = max(max_widths[i], self.get_len(col))

        if is_nicetable:
            max_widths = [
                min(self.max_col_len, width) for width in max_widths]
            print_data_row = self.print_nice_data_row
        else:
            print_data_row = self.print_data_row

        self.print_horizontal_line(max_widths)
        # print header
        print_data_row(max_widths, self.headers)
        self.print_horizontal_line(max_widths)

        for row in self.data:
            print_data_row(max_widths, row)
        self.print_horizontal_line(max_widths)

    def print_horizontal_line(self, widths):
        segments = ['-' * (width + 2) for width in widths]
        self.print_func("+%s+" % '+'.join(segments))

    def print_data_row(self, widths, data_row):
        formatted_row = [" %-*s " % (width, col)
                            for width, col in zip(widths, data_row)]
        self.print_func("|%s|" % '|'.join(formatted_row))

    def print_verbose(self):
        if self.headers:
            max_header_len = max([len(header) for header in self.headers])
        else:
            max_header_len = 0

        for i, row in enumerate(self.data):
            self.print_func("*" * 27 + " %1d. row " % (i + 1) + "*" * 27)
            for header, col in zip(self.headers, row):
                self.print_func("%*s: %s" % (max_header_len, header, col))

    def print_nice_data_row(self, widths, data_row):
        # calculate the maximum of lines need for this row
        count_line = 1
        for width, col in zip(widths, data_row):
            col_len = self.get_len(col)
            if col_len > width:
                tmp = int(col_len / width)
                if col_len % width != 0:
                    tmp += 1
                count_line = max(count_line, tmp)

        # print them out
        for i in range(count_line):
            cells = []
            for width, col in zip(widths, data_row):
                col_len = self.get_len(col)
                spaces_used = i * width
                if col_len > spaces_used:
                    # We display the maximum number of characters for this
                    # column, or the number of characters still left to
                    # display if it's smaller
                    len_to_display = min(col_len - width * i, width)
                    text = col[spaces_used:spaces_used + len_to_display]
                    cells.append(text.replace('\t', ' ').replace('\n', ' '))
                else:
                    cells.append("")
            formatted = [" %-*s " % (width, col)
                            for width, col in zip(widths, cells)]
            self.print_func("|%s|" % '|'.join(formatted))

    def print_html_table(self, options):
        # print everything before the table
        html = """
<html>
<head>
    <title>{title}</title>
    <style>
    table {{
        border-collapse:collapse;
    }}
    table, tr, td, th {{
        border: 1px solid black;
        padding: 3px;
    }}
    th {{
        background: #333;
        color: white;
        font-size: 80%;
    }}
    tr:nth-child(even) {{
        background: #ccc;
    }}
    tr:nth-child(odd) {{
        background: #fff;
    }}

    </style>
</head>
<body>
<table style="border: 1px solid black">
{headers}
{rows}
</table>
{trailing_content}
<p>Created at {timestamp}</p>
</body>
</html>
        """

        title = options.get(self.OPTION_TITLE, "")
        trailing_content = options.get(
            self.OPTION_ADDITIONAL_TRAILING_CONTENT,
            "",
        )
        headers = "<tr><th>" + "</th><th>".join(self.headers) + "</th></tr>\n"

        html_rows = []
        for row in self.data:
            partial_html_row = "</td><td>".join(row)
            html_row = "<tr><td>" + partial_html_row + "</td></tr>"
            html_rows.append(html_row)

        rows = "\n".join(html_rows)

        timestamp = time.ctime()

        self.print_func(html.format(**locals()))

    def get_len(self, value):
        if not value:
            return 0
        else:
            return len(value)


def parse_intervals(s):
    """
    Parse a string to return the intervals the string represents.

    Example:
        >>> parse_intervals("1,2")
        [Interval(start=1,end=1,is_start_opened=False,is_end_opened=False), Interval(start=2,end=2,is_start_opened=False,is_end_opened=False)]
    """
    s = s.strip()
    if not s:
        return []

    interval_strs = [segment.strip() for segment in s.split(',')]
    intervals = []
    for interval_str in interval_strs:
        num_or_interval = interval_str.split('-', 1)
        if len(num_or_interval) == 1:
            s = e = int(num_or_interval[0])
        else:
            s = int(num_or_interval[0])
            e = int(num_or_interval[1])

        interval = mathlib.Interval(
            s,
            e,
            is_start_opened=False,
            is_end_opened=False,
        )
        intervals.append(interval)

    return intervals


def confirm(prompt, file=None):
    """Ask the console application user a yes/no question.

    The user is expected to enter "y" or "t" for Yes (True), and "n" or "f"
    for No (False). The response is case-insensitive.

    "yes", "no", "true" and "false" works as expected.

    If the user enters other values, the question is repeated.

    Args:
        prompt (str): The question to ask the user.
    Returns:
        bool: True if the user's response means Yes, False if the user's
            response means No.
    """
    old_stdout = None
    if file is not None:
        old_stdout = sys.stdout
        sys.stdout = file

    try:
        while True:
            ans = six.moves.input(prompt + " [y/N/t/F] ").lower()

            if ans in ("y", "yes", "t", "true"):
                return True
            if ans in ("n", "no", "f", "false"):
                return False
    finally:
        if old_stdout:
            sys.stdout = old_stdout

def choose_item(prompt, items):
    """Asks the console application user to choose an item from a list

    The user is expected to enter the n'th item from items, 1-based.

    If the user enters a wrong value, an error is printed and has to choose
    again.

    Args:
        prompt (str): The question to ask the user.
    Returns:
        int: The integer chosen by the user, 0-based.
    """
    n = len(items)
    num_of_digits = 0
    while n:
        n //= 10
        num_of_digits += 1

    while True:
        for i, item in enumerate(items):
            print("%*s) %s" % (num_of_digits, i + 1, item))

        ans = six.moves.input(prompt)

        try:
            choice = int(ans)
            if choice < 1 or choice > len(items):
                print("Choose items between 1 to %d", len(items))
                continue

            return choice - 1
        except ValueError:
            print("Choose items between 1 to %d", len(items))


class Capturing(list):
    """
    Captures the standard out in a context, so you can do something like:

    with Capturing() as output:
        subprocess.check_call("echo blah", shell=True)

    print(str(output).contains("blah")) # true
    """

    def __enter__(self):
      self._stdout = sys.stdout
      sys.stdout = self._stringio = StringIO()
      return self

    def __exit__(self, *args):
      self.extend(self._stringio.getvalue().splitlines())
      sys.stdout = self._stdout


if __name__ == "__main__":
    rows = [
        {'a': "apple", 'b': "boy"},
        {'a': "one", 'b': "two"},
    ]
    DataPrinter(rows).print_result()
