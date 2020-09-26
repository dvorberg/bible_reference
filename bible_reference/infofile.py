#!/usr/bin/env python
# -*- coding: utf-8; -*-

##  Copyright 2018–20 by Diedrich Vorberg <diedrich@tux4web.de>
##
##  All Rights Reserved
##
##  For more Information on orm see the README file.
##
##  This program is free software; you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation; either version 2 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program; if not, write to the Free Software
##  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
##
##  I have added a copy of the GPL in the file COPYING

"""
I’m writing my own datafile format here. That may seem like
overkill, but for special purposes special solutions make sense.

It’s a simplified CSV format, using the semicolon “;” as delimeter,
which may be quoted using \. A “#” and everything after it is
considered a comment. “#”, too, may be quoted using a \. Empty lines
are ignored. Column values are stripped of whitespace left and
right. Encoding is UTF-8.

There are two subspecies: A regular or “list” datafile is just what
one would expect. In a “dict” datafile, the first line must start with a
“+” and contains the column headers/dict keys. There are two classes
for these two files. The presence/absence “+” is verifed by either
class. If you want a regular list with a “+” as the first sign of the
first value, er…, well, you can’t. 

The objects are read-only containers.
"""
from __future__ import print_function, unicode_literals
import re, io

__infofile_encoding__ = "utf-8"

class ParseError(Exception):
    """
    Raised when an error is found in an info file.
    """
    def __init__(self, filename, lineno, line, message):
        self.filename = filename
        self.lineno = lineno
        self.line = line
        self.message = message

    def __str__(self):
        return "%s:%i %s" % ( self.filename, self.lineno, self.message, )

class EmptyRow(Exception):
    """
    Raised by parse_row() if “line” is empty (or only a comment).
    """
    pass

_delimiter_re = re.compile(r"(?<!\\)([#;])")
_backslash_re = re.compile(r"\\(?=[#;])")
def parse_row(line):
    parts = _delimiter_re.split(line)
    parts = [_backslash_re.sub("", s) for s in parts]
    parts = [s.strip() for s in parts]
    parts = tuple(parts)
    
    if (not parts) or (parts[0] == "" and (
            len(parts) == 1 or parts[1] == "#")):
        raise EmptyRow()
        
    parts = iter(parts)
    while True:
        yield next(parts)
        try:
            delimiter = next(parts)
        except StopIteration:
            break
        else:
            if delimiter == "#":
                break

            
class Infofile:
    """
    Read a regular infofile with the format specified above and
    implement a read-only interface to a list of tuples.
    """    
    def __init__(self, filepath_or_fp):
        """
        """
        if isinstance(filepath_or_fp, io.IOBase):
            fp = filepath_or_fp
            filepath = repr(filepath_or_fp)
        else:
            fp = io.open(filepath_or_fp, encoding=__infofile_encoding__)
            filepath = filepath_or_fp
                        
        self._rows = []
        colcount = None

        for idx, line in enumerate(fp.readlines()):
            try:
                row = tuple(parse_row(line))
            except EmptyRow:
                pass
            else:                    
                if colcount is not None and len(row) != colcount:
                    raise ParseError(
                        filepath, idx+1, line,
                        "Mismatched number of columns %i instead of %i" % (
                            len(row), colcount))
                else:
                    colcount = len(row)

                self._rows.append(row)
                
        fp.close()
                
    def __len__(self): return self._rows.__len__()
    def __getitem__(self, idx): return self._rows.__getitem__(idx)
    def __reversed__ (self): return self._rows.__reversed__()    
    def __contains__(self): return self._rows.__contains__()        
    def __iter__(self): return self._rows.__iter__()

class DictInfofile:
    """
    Read an infofile that represents a read-only list of dicts, with
    the first row providing dict keys. The first entry in the first
    row must have a “+” as first character, which will be discarded.
    """
    def __init__(self, filepath_or_fp):
        """
        """
        if isinstance(filepath_or_fp, io.IOBase):
            fp = filepath_or_fp
            filepath = repr(filepath_or_fp)
        else:
            fp = io.open(filepath_or_fp, encoding=__infofile_encoding__)
            filepath = filepath_or_fp

        plus = fp.read(1)
        if plus != "+":
            raise IOError("Not a dict info file. (There is no +).")
            
        inif = iter(Infofile(fp))

        keys = next(inif)
        self._entries = []
        for tpl in inif:
            self._entries.append(dict(zip(keys, tpl)))
        
    def __len__(self): return self._entries.__len__()
    def __getitem__(self, idx): return self._entries.__getitem__(idx)
    def __reversed__ (self): return self._entries.__reversed__()    
    def __contains__(self): return self._entries.__contains__()        
    def __iter__(self): return self._entries.__iter__()

