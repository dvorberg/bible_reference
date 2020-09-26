# bible_reference
Parse, sort and pretty-print Bible references.

This module implements classes that I have developed to parse and
output Bible references. With some 3,000 years of literary history,
that’s not as simple a task as one might think, especially when
dealing with several languages. Rudimentary datafiles for English are
supplied, but the most detailed representation is for my native 
German.

**If you have any questions or suggestions, contact me at 
Diedrich Vorberg ‹[diedrich@tux4web.de](mailto:diedrich@tux4web.de)›!**

# Some introduction

## infofile.py

Information is stored in a special CSV-like textfile format documented
in the infofile.py.

## bible_reference.py

### bible_reference.Canon

A canon is the representation of an order of Biblical Books loaded
from a .canon (info-) file. 

There is an internal (default) naming-scheme for Biblical books that
consists of mostly tow-letter English abbreviations. That’s hardcoded
in the info-files, not so much in the Python code. The order
of the books in the .canon file will be the sort order of the books.
**These internal names are refered to throughout the code as a book’s `intid`.**

### bible_reference.BiblicalBook

Implement comparison (that is: sorting) of biblical books by canon
order.

### bible_reference.NamingScheme

Return an intid for a Biblical book and provide unified
human-readable representations.

### bible_reference.bible_reference_re()

Return a regular expression object matching Bible references that use
names from any of the naming schemes. Ordinals will not be checked
(“9.Cor” will match) nor key plausibility (meaning, ambigious naming
schemes will yield undefined results).

The resulting regex should match German („1.Kor 2,12“) and English
(1Cor 2:12) biblical references. **Your milage for English references
may vary, for it has not been tested extensively.**

### bible_reference.BibleReference

Here is where it all comes together. An instance is created using

```python
br = BibleReference(BiblicalBook("Jn"), 3, 16)
```

or

```python
from bible_reference import BibleReference
from bible_reference.naming_schemes import RGG, Luther84_abbr

br = BibleReference.parse("Joh 3,16", [ Luther84_abbr, RGG, ])
```

For represenration, the first naming scheme passed to the constructor
is used by default.


There is a directory postgresql/ containing example code on how to use
this for sorting biblical references in the a relational database in
canonical order. See [postgresql/README.md](postgresql/README.md)
