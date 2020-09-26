from bible_reference import BibleReferenceParser
from bible_reference.naming_schemes import RGG_abbr, Luther84, Luther84_abbr, \
    SBL_abbr

# Creating the BibleReferenceParser here will keep all the data in memory,
# organized and (the regular expressions) parsed. These are expensive
# operations that mast not be performed on each call of the plpython
# function.

parser = BibleReferenceParser(
    naming_schemes=[RGG_abbr, Luther84, Luther84_abbr])

def parse_bibref(reference):
    return parser.parse(reference)
    
def anglicize_bibref(reference):
    br = parser.parse(reference)
    return br.represent_using(SBL_abbr)
