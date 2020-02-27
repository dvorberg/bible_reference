# -*- coding: utf-8; -*-
from __future__ import print_function, unicode_literals
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
