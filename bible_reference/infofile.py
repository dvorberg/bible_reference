#!/usr/bin/env python
# -*- coding: utf-8; -*-

##  This file is part of the t4 Python module collection. 
##
##  Copyright 2018 by Diedrich Vorberg <diedrich@tux4web.de>
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
one’d expect. In a “dict” datafile, the first line must start with a
“+” and contains the column headers/dict keys. There are two classes
for these two files. The presence/absence “+” is verifed by either
class. If you want a regular list with a “+” as the first sign of the
first value, er…, well, you can’t. 

The objects are read-only containers.
"""
import string, types, re

class ParseError(Exception):
    def __init__(self, filename, lineno, line, message):
        self.filename = filename
        self.lineno = lineno
        self.line = line
        self.message = message

    def __str__(self):
        return "%s:%i %s" % ( self.filename, self.lineno, self.message, )

# Hardcoding the UTF-8 charset for this file-format.
# Like this, I decided a bunch of things in my Steve Jobs-like omnipotence. 
py_unicode = unicode
def unicode(s):
    return py_unicode(s, "utf-8")

class EmptyRow(Exception):
    """
    Raised by parse_row() if “line” is empty (or only a comment).
    """
    pass

delimiter_re = re.compile(r"(?<!\\)([#;])")
backslash_re = re.compile(r"\\(?=[#;])")
def parse_row(line):
    parts = delimiter_re.split(line)
    parts = map(lambda s: backslash_re.sub("", s), parts)
    parts = map(string.strip, parts)
    
    if (not parts) or (parts[0] == "" and (
            len(parts) == 1 or parts[1] == "#")):
        raise EmptyRow()
        
    parts = iter(parts)
    while True:
        yield parts.next()
        try:
            delimiter = parts.next()
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
        if type(filepath_or_fp) in (types.StringType, types.UnicodeType):
            fp = open(filepath_or_fp)
            filepath = filepath_or_fp
        else:
            fp = filepath_or_fp
            filepath = repr(filepath_or_fp)
            
        with open(filepath) as fp:
            self._rows = []
            colcount = None
            
            for idx, line_s in enumerate(fp.readlines()):
                line = unicode(line_s)
                try:
                    row = tuple(parse_row(line))
                except EmptyRow:
                    pass
                else:                    
                    if colcount is not None and len(row) != colcount:
                        raise ParseError(
                            filepath, idx+1, line_s,
                            "Mismatched number of columns %i instead of %i" % (
                                len(row), colcount))
                    else:
                        colcount = len(row)

                    self._rows.append(row)
                
        self.__len__ = self._rows.__len__
        self.__getitem__ = self._rows.__getitem__
        self.__iter__ = self._rows.__iter__
        self.__reversed__ = self._rows.__reversed__
        self.__contains__ = self._rows.__contains__




class dict_infofile:
    """
    Read an infofile that represents a read-only list of dicts, with
    the first row providing dict keys. The first entry in the first
    row must have a “+” as first character, which will be discarded.
    """
    def __init__(self, filepath_or_fp):
        inff = infofile(filepath_or_fp)
        if inff[0][0][0] != "+":
            raise IOError("Not a dict info file. (There is no +).")
        keys = inff[0]
        keys[0] = keys[0][1:] # Remove the +

        self._enrtries = []
        for tpl in inff[1:]:
            self._entries.append(dict(zip(keys, tpl)))
        
        self.__len__ = self._entries.__len__
        self.__getitem__ = self._entries.__getitem__
        self.__iter__ = self._entries.__iter__
        self.__reversed__ = self._entries.__reversed__
        self.__contains__ = self._entries.__contains__

        
# if __name__ == "__main__":
#     print(tuple(parse_row("Eins;Zwei;Dies \; ist ein Semikolon und \n dies \# ein Nummernkreuz # Ich bin der Kommentar #\n")))
#     #print tuple(parse_row("\n"))
#     #print tuple(parse_row("# I’m just a comment!\n"))
#     print(tuple(parse_row(";empty first col\n")))
#     print(tuple(parse_row(";\n")))
    
#     # i = Infofile("default.canon")
#     # print list(i)
