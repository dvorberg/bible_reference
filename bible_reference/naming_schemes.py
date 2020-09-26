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
Convenience module.
"""

from .bible_reference import NamingScheme

class LazyNamingScheme:
    """
    THe naming-schemes are there, but they are only loaded from their
    info file, if needed.
    """
    def __init__(self, name, ordinal_delimiter=".", verse_delimiter=","):
        self._lazy = ( name, ordinal_delimiter, verse_delimiter, )
        self.naming_scheme = None
    
    def __getattr__(self, name):
        if self.naming_scheme is None:
            n, ordinal, verse = self._lazy
            self.naming_scheme = NamingScheme.internal(n, ordinal, verse)
            
        return getattr(self.naming_scheme, name)
    
RGG = LazyNamingScheme("RGG")
RGG_abbr = LazyNamingScheme("RGG_abbr")
RGG_lang = LazyNamingScheme("RGG_lang")

Luther84 = LazyNamingScheme("Luther84")
Luther84_abbr = LazyNamingScheme("Luther84_abbr")

SBL = LazyNamingScheme("SBL", " ", ":")
SBL_abbr = LazyNamingScheme("SBL_abbr", " ", ":")
