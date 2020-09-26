#!/usr/bin/env python
# -*- coding: utf-8; -*-

##  This file is part of the t4 Python module collection. 
##
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

from __future__ import print_function, unicode_literals
import unittest
from bible_reference.bible_reference import (default_canon, BiblicalBook,
                                             NamingScheme, BibleReference)

class InfoFileTests(unittest.TestCase):
    def test_canon(self):
        dc = default_canon
        self.assertEqual(dc.book_ids[0], "Gn") # Genesis is the first book.
        self.assertEqual(dc.index["Gn"], 0)    # Genesis is the first book.

    def test_book(self):
        genesis = BiblicalBook("Gn")
        exodus = BiblicalBook("Ex")
        romans = BiblicalBook("Rm")

        self.assertTrue(genesis == BiblicalBook("Gn"))
        self.assertTrue(genesis < exodus)
        self.assertFalse(genesis > exodus)
        self.assertTrue(romans > exodus)
        self.assertTrue(exodus < romans)

    def test_naming_scheme(self):
        ns = NamingScheme.internal("RGG_abbr")
        genesis = BiblicalBook("Gn")
        romans = BiblicalBook("Rm")

        self.assertEqual(ns.intid_by_name[ (None, "Gen",) ], "Gn")
        # Die spinnen, die…
        self.assertEqual(ns.intid_by_name[ (None, "Röm",) ], "Rm")

        genesis = BiblicalBook("Gn")
        self.assertEqual(ns.name_for(genesis), "Gen")
        
        self.assertEqual(ns.intid_of(None, "Gen"), "Gn")
        self.assertEqual(ns.intid_of("1", "Kor"), "1Cor")
        self.assertEqual(ns.intid_of(None, "Röm"), "Rm")

        self.assertEqual(ns.book_named(None, "Gen"), genesis)
        self.assertEqual(ns.book_named(None, "Röm"), romans)

        self.assertEqual(ns.names(default_canon),
                         ("Gen", "Ex", "Lev", "Num", "Dtn", "Jos", "Ri",
                          "Ruth", "1Sam", "2Sam", "1Kön", "2Kön", "1Chr",
                          "2Chr", "Esr", "Neh", "Tob", "Jdt", "Est",
                          "1Makk", "2Makk", "3Makk", "4Makk", "Hi", "Ps",
                          "Spr", "Pred", "Hhld", "SapSal", "Sir", "Jes",
                          "Jer", "Klgl", "Bar", "Ez", "Dan", "Hos", "Jo",
                          "Am", "Ob", "Jon", "Mi", "Nah", "Hab", "Zeph",
                          "Hag", "Sach", "Mal", "Mt", "Mk", "Lk", "Joh",
                          "Apg", "Röm", "1Kor", "2Kor", "Gal", "Eph", "Phil",
                          "Kol", "1Thess", "2Thess", "1Tim", "2Tim", "Tit",
                          "Phil", "Heb", "Jak", "1Petr", "2Petr",
                          "1Joh", "2Joh", "3Joh", "Jud", "Apk"))

    def test_reference(self):
        genesis = BiblicalBook("Gn")
        exodus = BiblicalBook("Ex")
        john = BiblicalBook("Joh")
        romans = BiblicalBook("Rm")        

        creation = BibleReference(BiblicalBook("Gn"), 1, 1)
        burning_bush = BibleReference(BiblicalBook("Ex"), 3, 2)
        word_becomes_flesh = BibleReference(BiblicalBook("Jn"), 1, 14)
        faith_alone = BibleReference(BiblicalBook("Rm"), 3, 22)

        self.assertEqual(BibleReference.parse("Gen 1,1"), creation)
        self.assertEqual(BibleReference.parse("Ex 3,2"), burning_bush)
        self.assertEqual(BibleReference.parse("Joh 1,14"), word_becomes_flesh)
        self.assertEqual(BibleReference.parse("Röm 3,22"), faith_alone)

        
                                            
        
if __name__ == '__main__':
    unittest.main()    
