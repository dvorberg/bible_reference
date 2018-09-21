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

import types, re, os.path as op
from infofile import Infofile

from exceptions import CanonMismatch, BibleReferenceParseError

def here(filename, extension):
    if ("/") in filename:
        return filename
    else:
        return op.join(op.dirname(__file__), filename + extension)

class Canon:
    """
    A canon is the representation of an order of Biblical Books loaded
    from a .canon (info-) file.
    """
    def __init__(self, name):
        self.name = name
        self.book_ids = map(lambda (intid,):intid,
                            Infofile(here(name, ".canon")))
        self.index = dict(map(lambda (idx, intid): (intid, idx,),
                              enumerate(self.book_ids)))

    def __iter__(self):
        """
        Iterating over a canon will iterate over the book_ids in
        canonical order.
        """
        return iter(book_ids)

default_canon = Canon("default")

ordinal_re = re.compile(r"([0-9])?[\.\s]*(.*)", re.UNICODE)
class BiblicalBook:
    """
    Implement comparison (that is: sorting) of biblical books by canon
    order.
    """
    def __init__(self, intid, canon=default_canon):
        self.intid = intid
        self.canon = canon

        match = ordinal_re.match(intid)
        ordinal, name = match.groups()
        self.has_ordinal = bool(ordinal)

    def __cmp__(self, other):
        assert other.canon == self.canon, CanonMismatch
        return cmp(self.canon.index[self.intid],
                   self.canon.index[other.intid])

    def __eq__(self, other):
        return (self.intid == other.intid)

class NamingScheme:
    def __init__(self, name, ordinal_delimiter="."):
        """
        @name: The name of this naming scheme
        @ordinal_delimiter: If the book has an ordinal in its name
            (1Cor, 2. Macc), specify which unicode characters should go
            between the number and the name.
        """
        self.name = name
        self.name_by_intid = dict(Infofile(here(name, ".names")))
        self._intid_by_name = None # See intid_by_name() below!
        self.ordinal_delimiter = ordinal_delimiter

    @property
    def intid_by_name(self):
        """
        On demand, this will create an internal index matching tuples of
        (string-) ordinals and names to internal ids. For books that
        don’t have an ordnial, the ordinal part will be None.
        """
        def item( (intid, name,) ):
            """
            Return the ordinal (or None) of the book and a normalized
            representation of the name (capitalized!)
            """
            ordinal, name = ordinal_re.match(name).groups()
            return (ordinal, name.capitalize()), intid,
        
        if self._intid_by_name is None:
            self._intid_by_name = dict(map(item, self.name_by_intid.items()))

        return self._intid_by_name
        
    def name_for(self, biblical_book):
        our_name = self.name_by_intid[biblical_book.intid]

        if biblical_book.has_ordinal:
            match = ordinal_re.match(our_name)
            ordinal, name = match.groups()
            return ordinal + self.ordinal_delimiter + name
        else:
            return our_name

    def intid_of(self, ordinal, name):
        if not ordinal:
            ordinal = None
        if type(name) != types.UnicodeType:
            name = unicode(name)            
        return self.intid_by_name[(ordinal, name.capitalize(),)]

    def book_named(self, ordinal, name, canon=default_canon):
        return BiblicalBook(self.intid_of(ordinal, name), canon=canon)

    def names(self, canon=None):
        """
        Return the names in this naming scheme, optionally sorted using a
        canon.
        """
        ret = self.name_by_intid.items()

        if canon is not None:
            ret.sort(lambda a, b: cmp(canon.index[a[0]],
                                      canon.index[b[0]]))
        
        return map(lambda (intid, name,): name, ret)
        

# In the future the defaul twill be English, I think.
default_naming_scheme = NamingScheme("RGG_abbr")


_bible_reference_re_tmpl = ur"""
(?P<reference>
  (?:(?:(?P<ordinal>\d)[\.\s]?\s*)?(?P<book>%s))
                                        # Buch (das wird aus der DB gebaut!!)
  \s*
  (?P<range>
    (?P<parsable_range>
    \(?
    (?P<chapter>[0-9]+)                         # Kapitel
    (?:                                   # Alles nach dem Kapitel ist optional.
      (?:[,:]\(?(?P<v_start>\d+)[-–](?P<c_end>\d+),(?P<v_end>\d+)\)?)   # Röm 3,1-3,3
      |(?:[,:]\(?(?P<verse_range>\d+)[-–](?P<verse_range_end>\d+)\?)> # Röm 3,1-3
      |(?:[,:]\(?(?P<verse>\d+)f0,2}\)?)                             # Röm 3,1
      |(?:[-–](?P<chapter_range>\d+)f{0,2})                          # Röm 1-3
    )?                                    # …„nach dem Kapitel“-Gruppe
    \)?
    ) # parsable_range
    (?P<more>\s*[;\.\(\d\+][-–;\s\d\.\(\)f]*[\d\)])?
    \)?
  )
)
"""

def bible_reference_re(naming_schemes = [default_naming_scheme,]):
    """
    Return a regular expression object matching Bible references that
    use names from any of the naming schemes. Ordinals will not be
    checked (“9.Cor” will match) and nor key plausibility. In other
    words: If the naming schemes are ambiguous, you have to figure
    that out by yourseld.
    """
    names = set()
    for ns in naming_schemes:
        pairs = map(lambda name: ordinal_re.match(name).groups(),
                    ns.names())
        without_ordinals = map(lambda (ordinal, name): name, pairs)
        names = names.union(set(without_ordinals))

    names = "|".join(names)
    return re.compile(_bible_reference_re_tmpl % names,
                      re.VERBOSE | re.UNICODE)


class BibleReference:
    """
    Represent a bible reference for sorting and representation.

    “Chapter” and “verse” are integers (or none) for sorting, “range”
    is used for representation. Naming schemes can be provided for
    long names (“names”) and abbreviations (“abbrs”).
        
    @book: BiblicalBook instance
    @chapter: (something that parses to an) integer or None
    @verse: (something that parses to an) integer or None
    @range: String, a human-readable representation of the
       chapters/verses referenced. May be ''.
    """
    whitespace_re = re.compile(r"\s+", re.UNICODE)
    
    def __init__(self, book, chapter, verse, range,
                 names=default_naming_scheme):
        assert isinstance(book, BiblicalBook), TypeError
        self.book = book
        
        if chapter is not None:
            chapter = int(chapter)            
        self.chapter = chapter

        if verse is not None:
            verse = int(verse)
        self.verse = verse

        if range:
            # Normalize the human-readable range: All whitespace are (one)
            # regular space, all dashes are typographically correct “–”s.
            range = range.replace(u"-", u"–")
            range = self.whitespace_re.sub(" ", range)
            range = range.lower()
            
        self.range = range

        self.names = names
        
    @classmethod
    def parse(BibleReference, s, naming_schemes=[]):
        """
        Parse the bible reference in (unicode) string s using
        naming_schemes. The first naming scheme is used to construct
        the BibleReference returned.
        """
        if type(s) != types.UnicodeType:
            s = unicode(s)

        regex = bible_reference_re(naming_schemes)
        match = regex.match(s)
        if match is None:
            raise BibleReferenceParseError(s)
        else:
            d = match.groupdict()
            ret = BibleReference._from_match(match, naming_schemes)
            return ret

    @classmethod
    def finditer(BibleReference, s, naming_schemes=[]):
        if type(s) != types.UnicodeType:
            s = unicode(s)

        regex = bible_reference_re(naming_schemes)

        for match in regex.finditer(s):
            yield BibleReference._from_match(match, naming_schemes)

    @classmethod
    def _from_match(BibleReference, match, naming_schemes):
        groups = match.groupdict()

        for ns in naming_schemes:
            try:
                book = ns.book_named(groups[u"ordinal"], groups[u"book"])
                break
            except KeyError:
                pass

        chapter = groups[u"chapter"]
            
        verse = None
        if groups[u"verse"] is not None:
            verse = groups[u"verse"]
        elif groups[u"verse_range"] is not None:
            verse = groups[u"verse_range"]
        elif groups[u"v_start"] is not None:
            verse = groups[u"v_start"]
        
        return BibleReference(book, chapter, verse, groups[u"range"],
                              naming_schemes[0])
        
    def __str__(self):
        """
        The default string representation
        """
        return self.represent_using(self.names)

    def __repr__(self):
        return "<%s %s:%s '%s'>" % ( self.book.intid, self.chapter, self.verse,
                                     str(self.range), )
    
    def represent_using(self, naming_scheme):
        if (self.range):
            return "%s %s" % ( naming_scheme.name_for(self.book),
                               self.range, )
        else:
            return naming_scheme.name_for(self.book)

    def __cmp__(self, other):
        """
        For sorting.
        This might raise CanonMismatch from BiblicalBook.__cmp__().
        """
        return cmp( (self.book, self.chapter, self.verse,),
                    (other.book, other.chapter, other.verse,) )

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        
        return ( self.book == other.book and \
                 self.range == other.range )
    
