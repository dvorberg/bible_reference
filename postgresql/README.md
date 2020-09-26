One of my aims with this module is to retrieve database results on
biblical references in canonical order. This is implemented by parsing
the references into a Python-object and then using
`BiblicalReference.int_sort_index()` to calculate a 24-bit integer with
  - 8bit index of book in canon
  - 8bis chapter number
  - 8bits verse number
Sorted by these integers, the result will be in canonical order.

Parsing is an expensive operation. Large datasets will greatly benefit
from using SQL’s `CREATE INDEX`. Also you might want to create a
custom module that imports the relevant modules from this package and
creates a `BibleReferenceParser` object at load time. PostgreSQL will
create one Python interpreter per connection (I believe). So this
module will be loaded and unloaded a lot. But it’s still better than
loading the modules and initializing the parser each time the SQL
FUNCTION is called. 

**Steps**
- You will have to install the bible_reference package into the
  Python 3 installation your PostgreSQL server uses. (A `virtualenv`
  is advisable!)
- Create custom module in that installation site-packages/
  directory. Perhaps use my_bibref_module.py as a starting point.
- See `schema.sql` for an example on how to define the language and an 
  appropriate function in SQL.
  
You’re set to go!

If you want to create your own database, use my insert.py script to
upload some demo data. Then try:

```sql
SELECT reference, bibref_index(reference) FROM watchwords 
 ORDER BY bibref_index(reference);
```

```
     reference     | bibref_index 
-------------------+--------------
 Psalm 31,16a      |      1646352
 Psalm 33,12       |      1646860
 Ps 66,5           |      1655301
 Psalm 66,20       |      1655316
 Psalm 98,1        |      1663489
 Psalm 103,2       |      1664770
 Psalm 111,4       |      1666820
 Psalm 130,4       |      1671684
 Spr 14,34         |      1707554
 . . .
```

And if you don’t like (or can’t read) my German abbreviations, this
might do the trick:

```sql
SELECT reference, anglicize_bibref(reference), 
       bibref_index(reference) FROM watchwords
 ORDER BY bibref_index(reference);
```

```
 . . .
 Röm 12,21         | Rom 12:21          |      3542037
 1Kor 4,5b         | 1 Cor 4:5b         |      3605509
 2Kor 5,10         | 2 Cor 5:10         |      3671306
 2Kor 5,17         | 2 Cor 5:17         |      3671313
 Gal 6,2           | Gal 6:2            |      3737090
 Eph 2,8           | Eph 2:8            |      3801608
 Eph 2,19          | Eph 2:19           |      3801619
 . . . 
```

This uses the SBL_abbr naming scheme to represent the parsed bible
references. You milage may vary! Especially complex references may
result in strange things. But for something as simple es there
watchwords it just might work. 

Tell me what you think and if this is working for you!
