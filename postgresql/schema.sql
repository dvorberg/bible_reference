DROP TABLE IF EXISTS watchwords;
CREATE TABLE watchwords (
    reference TEXT
);

CREATE OR REPLACE FUNCTION plpython3_call_handler()
   RETURNS language_handler AS '$libdir/plpython3.so' LANGUAGE 'c';

CREATE OR REPLACE LANGUAGE 'plpython' HANDLER plpython3_call_handler;

CREATE OR REPLACE FUNCTION bibref_index (reference text)
  RETURNS int4
AS $$
    from my_bibref_module import parse_bibref
    return parse_bibref(reference).int_sort_index()
$$ LANGUAGE plpython;

CREATE OR REPLACE FUNCTION anglicize_bibref (reference text)
  RETURNS text
AS $$
    from my_bibref_module import anglicize_bibref
    return anglicize_bibref(reference)
$$ LANGUAGE plpython;
