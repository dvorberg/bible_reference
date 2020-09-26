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
This module implements classes that I have developed to parse and
output Bible references. With some 3,000 years of literary history
that’s not as simple a task as one might think, especially when
dealing with several languages. Rudimentary datafiles for English are
supplied, but the most detailed representation is for my native tongue
German.
"""

from .bible_reference import here, Canon, NamingScheme, BiblicalBook, \
    BibleReference

