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
Main module containing classes Canons, biblical Books, naming
schemes and the class that binds it all together: BibleReference.
"""

from __future__ import print_function, unicode_literals
import re, os.path as op, collections, numbers, functools

from .infofile import Infofile

class CanonMismatch(Exception):
    """
    Raised, if biblical books sorted, that are not in the same canon.
    """

class BibleReferenceParseError(Exception):
    """
    Bible Reference Parse Error
    """

def here(filename, extension):
    if ("/") in filename:
        return filename
    else:
        return op.join(op.dirname(__file__), filename + extension)

reference_int_re = re.compile(r"(\d+)[abcdf]?")
def reference_int(s):
    """
    Accept input that has “f” or ”a“, ”b“… attached to a number.
    """
    if isinstance(s, numbers.Number):
        return int(s)
    else:
        match = reference_int_re.match(s)
        if match is None:
            raise ValueError(
                "invalid literal for reference_int() with base 10: '%s'" % s)
        else:
            q, = match.groups()
            return int(q)
    
    
class Canon:
    """
    A canon is the representation of an order of Biblical Books loaded
    from a .canon (info-) file.
    """
    def __init__(self, name):
        self.name = name
        self.book_ids = tuple(
            [tpl[0] for tpl in Infofile(here(name, ".canon"))])
        self.index = dict(
            [(tpl[1], tpl[0],) for tpl in enumerate(self.book_ids)])

    def __iter__(self):
        """
        Iterating over a canon will iterate over the book_ids in
        canonical order.
        """
        return iter(book_ids)

default_canon = Canon("default")

ordinal_re = re.compile(r"([0-9])?[\.\s]*(.*)", re.UNICODE)

@functools.total_ordering
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
        
    def __eq__(self, other):
        return (self.intid == other.intid)

    def __lt__(self, other):
        assert other.canon == self.canon, CanonMismatch
        return self.canon.index[self.intid] < self.canon.index[other.intid]

    def __gt__(self, other):
        assert other.canon == self.canon, CanonMismatch
        return self.canon.index[self.intid] > self.canon.index[other.intid]

class NamingScheme:
    """
    Return an intid for a Biblical book and provide unified
    human-readable representations.
    """
    def __init__(self, name_by_intid, name=None,
                 ordinal_delimiter=".", verse_delimiter=","):
        """
        @name_by_intid: Dict matching internal ids to book names.
        @name: The name of this naming scheme; defaults to internal id.
        @ordinal_delimiter: If the book has an ordinal in its name
            (1Cor, 2. Macc), specify which unicode characters should go
            between the number and the name.
        @verse_delimiter: Characer(s) put between chapter and verse
            in a reference, as in “John 2<verse_delimiter>12”.
        """
        if not name:
            self.name = "<%s %i>" % ( self.__class__.__name__, id(self), )
        else:            
            self.name = name

        if not isinstance(name_by_intid, collections.Mapping):
            raise TypeError("name_by_intid must be Mapping type")
        else:
            self.name_by_intid = name_by_intid
        
        self.ordinal_delimiter = ordinal_delimiter
        self.verse_delimiter = verse_delimiter

        self._intid_by_name = None

    @classmethod
    def internal(cls, name, ordinal_delimiter=".", verse_delimiter=","):
        """
        @name: The name of this naming scheme matching .names file
            distributed in this directory.
        @ordinal_delimiter: If the book has an ordinal in its name
            (1Cor, 2. Macc), specify which unicode characters should go
            between the number and the name.
        @verse_delimiter: Unicode characters but between chapter and verse
            in a reference, as in “John 2<verse_delimiter>12”.
        """
        return cls.from_infofile(here(name, ".names"), name,
                                 ordinal_delimiter, verse_delimiter)

    @classmethod
    def from_infofile(cls, filepath, name=None,
                      ordinal_delimiter=".", verse_delimiter=","):
        """
        @filepath: Path to .info file, formatted like the .names files
            from this project.
        @name: The name of this naming scheme . 
        @ordinal_delimiter: If the book has an ordinal in its name
            (1Cor, 2. Macc), specify which unicode characters should go
            between the number and the name.
        @verse_delimiter: Unicode characters but between chapter and verse
            in a reference, as in “John 2<verse_delimiter>12”.
        """
        if name is None:
            fname = op.basename(filepath)
            name, ext = op.splitext(fname)

        return cls(dict(Infofile(filepath)), name,
                   ordinal_delimiter, verse_delimiter)
    
    @property
    def intid_by_name(self):
        """
        On demand, this will create an internal index matching tuples of
        (string-) ordinals and names to internal ids. For books that
        don’t have an ordnial, the ordinal part will be None.
        """
        def item(tpl):
            """
            Return the ordinal (or None) of the book and a normalized
            representation of the name (capitalized!)
            """
            intid, name = tpl
            ordinal, name = ordinal_re.match(name).groups()
            return (ordinal, name.capitalize()), intid,
        
        if self._intid_by_name is None:
            self._intid_by_name = dict(
                [item(tpl) for tpl in self.name_by_intid.items()])

        return self._intid_by_name
        
    def name_for(self, biblical_book):
        """
        Return the pretty name for a BiblicalBook object.
        """
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
            
        return self.intid_by_name[(ordinal, name.capitalize(),)]

    def book_named(self, ordinal, name, canon):
        """
        Return a BiblicalBook object for the info provided.
        """
        return BiblicalBook(self.intid_of(ordinal, name), canon=canon)

    def names(self, canon=None):
        """
        Return the names in this naming scheme as tuple, optionally sorted
        using a canon.
        """
        ret = self.name_by_intid.items()

        # ret is a list of tuples as ( intid, name, )        
        if canon is not None:
            ret = sorted(ret, key=lambda tpl: canon.index[tpl[0]])
        
        return tuple([tpl[1] for tpl in ret])
        

default_naming_scheme = NamingScheme.internal("default")
def set_default_naming_scheme(naming_scheme):
    global default_naming_scheme
    default_naming_scheme = naming_scheme

_bible_reference_re_tmpl = r"""
(?P<reference>
  (?:(?:(?P<ordinal>\d)[\.\s]?\s*)?(?P<book>%s))
                                        # Buch (das wird aus der DB gebaut!!)
  \s*
  (?P<range>
    (?P<parsable_range>
    \(?
    (?P<chapter>[0-9]+)                   # Kapitel
    (?:                                   # Alles nach dem Kapitel ist optional.
      (?:[,:]\(?(?P<v_start>\d+[ab]?)[-–](?P<c_end>\d+[ab]?),(?P<v_end>\d+[ab]?)\)?)   # Röm 3,1-3,3
      |(?:[,:]\(?(?P<verse_range>\d+[ab]?)[-–](?P<verse_range_end>\d+[ab]?)) # Röm 3,1-3
      |(?:[,:]\(?(?P<verse>\d+[ab]?)f{0,2}\)?)                            # Röm 3,1
      |(?:[-–](?P<chapter_range>\d+[ab]?)f{0,2})                          # Röm 1-3
    )?                                    # …„nach dem Kapitel“-Gruppe
    \)?
    ) # parsable_range
    (?P<more>\s*[;\.\(\d\+][-–;\s\dab\.\(\)f]*[\dab\)])?
    \)?
  )
)
"""

def bible_reference_re(naming_schemes=None):
    """
    Return a regular expression object matching Bible references that
    use names from any of the naming schemes. Ordinals will not be
    checked (“9.Cor” will match) nor key plausibility (meaning,
    ambigious naming schemes will yield undefined results).
    """
    if naming_schemes is None:
        naming_schemes = [ default_naming_scheme, ]
    
    names = set()
    for ns in naming_schemes:
        pairs = [ordinal_re.match(name).groups() for name in ns.names()]
        without_ordinals = [ordinal_name[1] for ordinal_name in pairs]
        names = names.union(set(without_ordinals))

    names = "|".join(names)
    return re.compile(_bible_reference_re_tmpl % names, re.VERBOSE)


class BibleReferenceParser:
    """
    To parse of find bible references from strings, an elaborate
    regular expression is constructed. For efficiency, this may be
    stored as a parser object.
    """
    def __init__(self, naming_schemes=None, canon=default_canon):
        if naming_schemes is None:
            self.naming_schemes = [ default_naming_scheme, ]
        else:
            self.naming_schemes = naming_schemes

        self.canon = canon
            
        self.regex = bible_reference_re(self.naming_schemes)

    def parse(self, s):
        """
        Parse s into a BibleReference object. May raise ParseError.
        """
        match = self.regex.match(s)
        if match is None:
            raise BibleReferenceParseError(s)
        else:
            return BibleReference._from_match(
                match, self.naming_schemes, self.canon)

    def finditer(self, s):
        """
        Iterate over all bible references that can be found in s.
        """
        for match in self.regex.finditer(s):
            yield BibleReference._from_match(
                match, self.naming_schemes, self.canon)



@functools.total_ordering
class BibleReference:
    """
    Represent a bible reference for sorting and representation.
    """
    whitespace_re = re.compile(r"\s+", re.UNICODE)
    
    def __init__(self, book, chapter, verse, range="", naming_scheme=None):
        """
        “Chapter” and “verse” are integers (or none) for sorting, “range”
        is used for representation. Naming schemes can be provided for
        long names (“names”) and abbreviations (“abbrs”).
        
        @book: BiblicalBook instance
        @chapter: (something that parses to an) integer or None
        @verse: (something that parses to an) integer or None
        @range: String, a human-readable representation of the
           chapters/verses referenced. May be ''.
        @naming_scheme: Used for representation. Defaults to
           bible_reference.default_naming_scheme.
        """
        assert isinstance(book, BiblicalBook), TypeError
        self.book = book
        
        if chapter is not None:
            chapter = reference_int(chapter)            
        self.chapter = chapter

        if verse is not None:            
            verse = reference_int(verse)
        self.verse = verse

        if range:
            # Normalize the human-readable range: All whitespace are (one)
            # regular space, all dashes are typographically correct “–”s.
            range = range.replace("-", "–")
            range = self.whitespace_re.sub(" ", range)
            range = range.lower()
            
        self._range = range
        self.naming_scheme = naming_scheme or default_naming_scheme

    @classmethod
    def parse(BibleReference, s, naming_schemes=None, canon=default_canon):
        """
        Parse the bible reference in s using naming_schemes. The first
        naming scheme is used to construct the BibleReference
        returned.
        
        @param naming_schemes: Defaults to
            bible_reference.default_naming_scheme.
        @param canon: The canon that will be associated with the bible
            references returned. Defaults to the default canon.
        """
        parser = BibleReferenceParser(naming_schemes, canon)
        return parser.parse(s)
    
    @classmethod
    def finditer(BibleReference, s, naming_schemes=None, canon=default_canon):
        """
        Search through `s` for Bible references using `naming_schemes`.
        
        @param naming_schemes: Defaults to
            bible_reference.default_naming_scheme.
        @param canon: The canon that will be associated with the bible
            references returned. Defaults to the default canon.
        """
        parser = BibleReferenceParser(naming_schemes, canon)
        for br in parser.finditer(s):
            yield br

    @classmethod
    def _from_match(BibleReference, match, naming_schemes, canon):
        groups = match.groupdict()

        book = None
        found_in_naming_scheme = naming_schemes[0]
        for ns in naming_schemes:
            try:
                book = ns.book_named(groups["ordinal"], groups["book"], canon)
                found_in_naming_scheme = ns
                break
            except KeyError:
                pass

        if book is None:
            raise KeyError("Unknown book: %(ordinal)s %(book)s" % groups)

        chapter = groups["chapter"]
            
        verse = None
        if groups["verse"] is not None:
            verse = groups["verse"]
        elif groups["verse_range"] is not None:
            verse = groups["verse_range"]
        elif groups["v_start"] is not None:
            verse = groups["v_start"]

        # Internally, we use “,” as a verse delimiter.
        if groups["range"]:
            range = groups["range"].replace(":", ",")
        else:
            range = None
            
        return BibleReference(book, chapter, verse, range, naming_schemes[0])

    @property
    def range(self):
        if self._range:
            return self._range
        else:
            if self.chapter and self.verse:
                return "%i,%i" % ( self.chapter, self.verse, )
            elif self.chapter:
                return "%i" % self.chapter
            else:
                return ""

    @range.setter
    def range(self, range):
        # Internally, we use “,” as a verse delimiter.
        range = range.replace(";", ",") 
        self._range = range
            
    def __str__(self):
        """
        The default string representation
        """
        return self.represent_using(self.naming_scheme)

    def __repr__(self):
        return "<%s %s:%s '%s'>" % ( self.book.intid, self.chapter, self.verse,
                                     self.range, )
    
    def represent_using(self, naming_scheme):
        if self.range:
            range = self.range
            if naming_scheme.verse_delimiter != ",":
                range = range.replace(",", naming_scheme.verse_delimiter)
            return "%s %s" % ( naming_scheme.name_for(self.book), range, )
        else:
            return naming_scheme.name_for(self.book)

    def __lt__(self, other):
        """
        For sorting.
        This might raise CanonMismatch from BiblicalBook.__cmp__().
        """
        return (self.book, self.chapter, self.verse,) < (other.book,
                                                         other.chapter,
                                                         other.verse,)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        
        return ( self.book == other.book and \
                 self.range == other.range )


    def int_sort_index(self):
        """
        Return an integer uniqly identifying this biblical reference for
        sorting. 24 bits will be used to represent
        - 8bit index of book in canon
        - 8bis chapter number
        - 8bits verse number
        """
        b = self.book.canon.index[self.book.intid] + 1
        c = self.chapter or 0
        v = self.verse or 0

        return b << 16 | c << 8 | v;
