#!/usr/bin/python
import matplotlib.pyplot as plot
import sys
import argparse
import sqlite3 as lite
import os

parser = argparse.ArgumentParser(description="Query databse for Yelp data (JSON formatted)")
parser.add_argument("database", help="Path to database file created with read_and_init_yelp_db.py")

try:
    args = parser.parse_args()
except SystemExit:
    parser.print_help()
    sys.exit()

if not os.path.exists(args.database):
    raise ValueError(args.database + " does not appear to exist!")

con = None
try:
    con = lite.connect(args.database, isolation_level=None)
    con.row_factory = lite.Row
    cur = con.cursor()

except lite.Error, e:
    print "Error %s:" % e.args[0]
    sys.exit(1)

cur.execute("SELECT * FROM review")
res = cur.fetchall()
for r in res:
    print r
print res[0].keys()
con.close()
