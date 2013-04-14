#!/usr/bin/python
import json
import matplotlib.pyplot as plot
import sys
import argparse
import sqlite3 as lite
import re

parser = argparse.ArgumentParser(description="Read in Yelp data (JSON formatted)")
parser.add_argument("business", help="Path to business file containing Yelp JSON data")
parser.add_argument("checkin", help="Path to checkin file")
parser.add_argument("review", help="Path to review file")
parser.add_argument("user", help="Path to user file")

try:
    args = parser.parse_args()
except SystemExit:
    parser.print_help()
    sys.exit()

def get_JSON_data(filepath, key, sub_key="business_id", prev_data={}):
    with open(filepath) as f:
        prev_data[key] = {}
        for line in f:
            converted_json = json.loads(line)
            prev_data[key][converted_json[sub_key]] = converted_json
    return prev_data

def create_db_tables(cur, fields_and_types_dict, name="Yelp"):
    def gen_table_string(d):
        return ",".join([str(x) + " " + str(d[x]) for x in sorted(d.keys())])
    table_string = gen_table_string(fields_and_types_dict)
    cur.execute("CREATE TABLE " + name + "("+table_string+")")

def fill_db(cur, all_data, fields_and_types_dict, name="Yelp"):
    fields = fields_and_types_dict.keys()
    data_categories = all_data.keys()
    #Don't use user data
    data_categories.remove("user")
    category_switch = {}
    for f in fields:
        for c in data_categories:
            if f in all_data[c][all_data[c].keys()[0]]:
                category_switch[f] = c

    business_ids = all_data[data_categories[0]].keys()
    for b in business_ids:
        try:
            v = []
            for f in sorted(fields):
                val = unicode(all_data[category_switch[f]][b][f])
                val = re.sub(r"\W","", val)
                v.append(val)
            sql_str = "INSERT INTO "+name+" VALUES ("+",".join(["?"]*len(v))+")"
            print sql_str
            print v
            cur.execute(sql_str,v)
        except KeyError:
            print "Unable to find value " + `f` + " for key " + `b`

def remove_from_list(l, entries):
    for e in entries:
        l.remove(e)
    return l

def gen_fields_and_types_dict(fields, int_fields=[], real_fields=[], blob_fields=[], text_fields=[], default_type="TEXT"):
    #List of types here: http://www.sqlite.org/datatype3.html
    fields_and_types_dict = {}
    for f in fields:
        fields_and_types_dict[f] = default_type
    for f in int_fields:
        fields_and_types_dict[f] = "INT"
    for f in real_fields:
        fields_and_types_dict[f] = "REAL"
    for f in blob_fields:
        fields_and_types_dict[f] = "BLOB"
    for f in text_fields:
        fields_and_types_dict[f] = "TEXT"
    return fields_and_types_dict

all_data = {}
all_data = get_JSON_data(args.business, "business", sub_key="business_id" ,prev_data=all_data)
all_data = get_JSON_data(args.checkin, "checkin", sub_key="business_id", prev_data=all_data)
all_data = get_JSON_data(args.review, "review", sub_key="business_id", prev_data=all_data)
all_data = get_JSON_data(args.user, "user", sub_key="user_id", prev_data=all_data)

con = None
#USE_MEMORY=True
USE_MEMORY=False
try:
    if USE_MEMORY:
        con = lite.connect(":memory:", isolation_level=None)
    else:
        con = lite.connect("yelp.db", isolation_level=None)
    cur = con.cursor()

except lite.Error, e:
    print "Error %s:" % e.args[0]
    sys.exit(1)

all_business_ids = all_data["business"].keys()
db_keys = []
db_keys.extend(all_data["business"][all_business_ids[0]].keys())
db_keys.extend(all_data["checkin"][all_business_ids[0]].keys())
db_keys = sorted(set(db_keys))

#db_keys look like this with all business categories (not user):
#[u'business_id', u'categories', u'checkin_info', u'city', u'date', u'full_address', u'latitude', u'longitude', u'name', u'neighborhoods', u'open', u'review_count', u'review_id', u'stars', u'state', u'text', u'type', u'user_id', u'votes']
#without review data
#[u'business_id', u'categories', u'checkin_info', u'city', u'full_address', u'latitude', u'longitude', u'name', u'neighborhoods', u'open', u'review_count', u'stars', u'state', u'type']
#ideal fields for db are
#[u'business_id', u'categories', u'city', u'full_address', u'latitude', u'longitude', u'review_count', u'stars', u'state', u'type']

db_keys = remove_from_list(db_keys, ["checkin_info","open","categories","neighborhoods"])
fields_and_types_dict = gen_fields_and_types_dict(db_keys, int_fields=["review_count","stars"], real_fields=["latitude","longitude"], blob_fields=["full_address"])
create_db_tables(cur, fields_and_types_dict)
fill_db(cur, all_data, fields_and_types_dict)

con.close()
