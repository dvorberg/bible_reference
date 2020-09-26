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

import unittest
from bible_reference.infofile import Infofile, DictInfofile

class InfoFileTests(unittest.TestCase):
    def test_normal(self):
        inf = Infofile("infofile_tests/normal.info")
        self.assertEqual(tuple(inf),
                         (('Erstens', 'Zweitens', 'Drittens'),
                          ('2.1', '2.2', '2.3')))

    def test_empty_fields(self):
        inf = Infofile("infofile_tests/empty_fields.info")
        self.assertEqual(tuple(inf), (('', ''),))

    def test_quoting(self):
        inf = Infofile("infofile_tests/quoting.info")
        self.assertEqual(
            tuple(inf),
            (('Eins', 'Zwei',
              'Dies ; ist ein Semikolon und \\n dies # ein Nummernkreuz'),
             ('1', '2', '3')))

    def test_unicode(self):
        inf = Infofile("infofile_tests/unicode.info")
        self.assertEqual(tuple(inf), (('λογός σάρχ ἐγένετο', 'üäöÜÄÖüäö'),))

    def test_mapping(self):
        inf = DictInfofile("infofile_tests/mapping.info")
        self.assertEqual(tuple(inf),
                         ({'int': '0', 'numeral': 'zero'},
                          {'int': '1', 'numeral': 'one'},
                          {'int': '2', 'numeral': 'two'},
                          {'int': '3', 'numeral': 'three'},
                          {'int': '4', 'numeral': 'four'},
                          {'int': '5', 'numeral': 'five'}))

    

if __name__ == '__main__':
    unittest.main()    
