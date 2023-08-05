#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Mon Jun 29 14:46:20 CEST 2020 -*-
# -*- copyright: GH/IPHC 2020 -*-
# -*- file: ascii_data_file/ascii_data_file.py -*-
# -*- purpose: -*-

'''
The AsciiDataFile object return float values from collumn formated text files

Us as : AsciiDataFile(filepath: str or list ,
                      fileappend or file side to side
                      comment_prefix: str = "#",
                      skip_empty_lines: bool = True,
                      return_cols: ['*' or slice or sequence] = '*',
                      return_type: type = float
                      separator: str = None
)
returns an iterable object
'''

from itertools import chain
from operator import itemgetter

from warnings import warn

from typing import Union, Sequence, Generator, Any


def data_file(file_path: Union[str, Sequence[str]],
              returned_columns: Union[str, slice, Sequence[int]] = '*',
              comment_prefix: str = "#",
              separator: Union[None, str] = None,
              returned_type: type = float,
              multi_files_behavior: str = 'append',
              skip_empty_lines: bool = True,
              skip_error_lines: bool = True,
              error_line_warning: bool = True,
              error_line_error: bool = False,
              *w, **kw) -> Generator[Any, None, None]:
    '''
Returns a generator filtering out commented lines

parameters:
        - `file_path` (str or list of str), required: the path to the file or files to open
        - `returned columns` (`'*'` or slice or list of int), default = '`'*'`: select the columns to return.
                either `'*'` for all, a list of indices, or a slice.
        - `separator` (None or str), default = None: the column separator (as used in str.split(sep))
        - `comment_prefix` (str), default = "#": the characters to look for at the start of a commented line.
        - `returned_type` (type), default = `float`: the type of data to return.
        - `multi_files_behavior` (str), default = 'append': what to do when multiple files are given in input.
                either `append` or `side_by_side`
        - `skip_empty_lines` (bool), default = True: wether to skip empty lines
        - `skip_error_lines` (bool), default = True: wether to skip files with errorin the processing
        - `error_line_warning` (bool), default = True: if error lines are not skipped, wether to issue a warning
        - `error_line_error` (bool), default = True: if error lines are not skipped, wether to raise a RuntimeError when there is a problem reading the line.
    '''
    def _line_unfold(is_multi: str,
                     the_line: Union[str, Sequence[str]],
                     separator: Union[None, str]) -> str:
        'tool func in case of multi file side by side'
        if is_multi == 'side_by_side':
            if separator is None:
                return " ".join(the_line)
            return separator.join(the_line)
        return the_line.strip()
    #
    if isinstance(file_path, str):
        _file_to_read = open(file_path, 'r')
    else:
        if multi_files_behavior == 'append':
            _file_to_read = chain(*map(open, file_path))
        elif multi_files_behavior == 'side_by_side':
            # put side to side
            _file_to_read = zip(*map(open, file_path))
        else:
            raise NotImplementedError
    while True:
        try:
            # Here I just want to point that using the walrus operator would be great
            new_line = _line_unfold(multi_files_behavior,
                                    next(_file_to_read),
                                    separator)
            while new_line.startswith(comment_prefix) \
                  or (skip_empty_lines and len(new_line.strip()) == 0):
                new_line = _line_unfold(multi_files_behavior,
                                        next(_file_to_read),
                                        separator)
            # Got the next line, now process
            this_line_elements = tuple(map(returned_type, new_line.split(separator)))
            if returned_columns == '*':
                yield this_line_elements
            elif isinstance(returned_columns, slice):
                yield this_line_elements[returned_columns]
            else:
                yield itemgetter(*returned_columns)(this_line_elements)
        except ValueError:
            if skip_error_lines:
                continue
            if error_line_warning:
                warn(f"One line could not be parsed: {new_line}")
                continue
            if error_line_error:
                raise RuntimeError
        except StopIteration:
            return


# EOF
