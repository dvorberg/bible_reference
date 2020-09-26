import argparse, getpass, psycopg2

"""
Create a table in a database and put bible references in it.
pp"""

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-d", metavar="dbname", default=getpass.getuser(),
                        required=True, dest="dbname",
                        help="Name of the PostgreSQL database to connect to ")

    args = parser.parse_args()
    
    conn = psycopg2.connect("dbname=%s" % args.dbname)


    with open("schema.sql") as fp:
        sql = fp.read()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

    
    with open("data.txt") as fp:
        cursor = conn.cursor()
        for line in fp.readlines():
            line = line.strip()
            if line:
                cursor.execute(f"INSERT INTO watchwords VALUES ( '{line}' )");
        conn.commit()
        

main()
