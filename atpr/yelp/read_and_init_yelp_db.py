#!/usr/bin/python
import json
import sys
import argparse
import sqlite3 as lite
import re

parser = argparse.ArgumentParser(description="Read in Yelp data (JSON formatted)")
parser.add_argument("business", help="Path to business file containing Yelp JSON data")
parser.add_argument("checkin", help="Path to checkin file")
parser.add_argument("review", help="Path to review file")
parser.add_argument("user", help="Path to user file")
parser.add_argument("-v", "--verbose", action="count", help="Verbosity, -v for verbose or -vv for very verbose")
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

def create_db_table(cur, fields_and_types_dict, name):
    def gen_table_string(d):
        return ",".join([str(x) + " " + str(d[x]) for x in sorted(d.keys())])
    table_string = gen_table_string(fields_and_types_dict)
    cur.execute("CREATE TABLE " + name + "("+table_string+")")

def fill_review_table(cur, all_data, fields_and_types_dict, name):
    fields = fields_and_types_dict.keys()
    data_categories = all_data.keys()
    data_categories.remove("checkin")
    data_categories.remove("business")
    data_categories.remove("user")
    #only use user data
    review_ids = all_data[data_categories[0]].keys()
    for r in review_ids:
        try:
            v = []
            for f in sorted(fields):
                val = unicode(all_data["review"][r][f])
                val = re.sub(r"\W","::", val)
                val = re.sub(r":u:","", val)
                v.append(val)
            sql_str = "INSERT INTO "+name+" VALUES ("+",".join(["?"]*len(v))+")"
            if args.verbose > 0:
                print sql_str
                print v
            cur.execute(sql_str,v)
        except KeyError:
            if args.verbose > 0:
                print "Unable to find value " + `f` + " for key " + `r`

def fill_user_table(cur, all_data, fields_and_types_dict, name):
    fields = fields_and_types_dict.keys()
    data_categories = all_data.keys()
    data_categories.remove("checkin")
    data_categories.remove("business")
    data_categories.remove("review")
    #only use user data
    user_ids = all_data[data_categories[0]].keys()
    for u in user_ids:
        try:
            v = []
            for f in sorted(fields):
                val = unicode(all_data["user"][u][f])
                val = re.sub(r"\W","::", val)
                val = re.sub(r":u:","", val)
                v.append(val)
            sql_str = "INSERT INTO "+name+" VALUES ("+",".join(["?"]*len(v))+")"
            if args.verbose > 0:
                print sql_str
                print v
            cur.execute(sql_str,v)
        except KeyError:
            if args.verbose > 0:
                print "Unable to find value " + `f` + " for key " + `u`

def fill_business_table(cur, all_data, fields_and_types_dict, name):
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
                val = re.sub(r"\W","::", val)
                v.append(val)
            sql_str = "INSERT INTO "+name+" VALUES ("+",".join(["?"]*len(v))+")"
            if args.verbose > 0:
                print sql_str
                print v
            cur.execute(sql_str,v)
        except KeyError:
            if args.verbose > 0:
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
bus_table_keys = []
bus_table_keys.extend(all_data["business"][all_business_ids[0]].keys())
bus_table_keys.extend(all_data["checkin"][all_business_ids[0]].keys())
bus_table_keys = sorted(set(bus_table_keys))

#table_keys look like this with all business categories (not user):
#[u'business_id', u'categories', u'checkin_info', u'city', u'date', u'full_address', u'latitude', u'longitude', u'name', u'neighborhoods', u'open', u'review_count', u'review_id', u'stars', u'state', u'text', u'type', u'user_id', u'votes']
#without review data
#[u'business_id', u'categories', u'checkin_info', u'city', u'full_address', u'latitude', u'longitude', u'name', u'neighborhoods', u'open', u'review_count', u'stars', u'state', u'type']
#ideal fields for table are
#[u'business_id', u'categories', u'city', u'full_address', u'latitude', u'longitude', u'review_count', u'stars', u'state', u'type']

bus_table_keys = remove_from_list(bus_table_keys, ["checkin_info","open","categories","neighborhoods"])
bus_table_name = "business"
fields_and_types_dict = gen_fields_and_types_dict(bus_table_keys, int_fields=["review_count","stars"], real_fields=["latitude","longitude"])
create_db_table(cur, fields_and_types_dict, bus_table_name)
fill_business_table(cur, all_data, fields_and_types_dict, bus_table_name)

all_user_ids = all_data["user"].keys()
user_table_keys = []
user_table_keys.extend(all_data["user"][all_user_ids[0]].keys())
user_table_keys = sorted(set(user_table_keys))

#Ideal user table fields
#[u'average_stars', u'name', u'review_count', u'type', u'user_id', u'votes']

user_table_name="user"
fields_and_types_dict = gen_fields_and_types_dict(user_table_keys, int_fields=["review_count", "votes"], real_fields=["average_stars"])
create_db_table(cur, fields_and_types_dict, user_table_name)
fill_user_table(cur, all_data, fields_and_types_dict, user_table_name)

all_review_ids = all_data["review"].keys()
review_table_keys = []
review_table_keys.extend(all_data["review"][all_review_ids[0]].keys())
review_table_keys = sorted(set(review_table_keys))

#Ideal review fields
#[u'business_id', u'date', u'review_id', u'stars', u'text', u'type', u'user_id', u'votes']

review_table_name="review"
fields_and_types_dict = gen_fields_and_types_dict(review_table_keys, int_fields=["votes"], real_fields=["stars"])
create_db_table(cur, fields_and_types_dict, review_table_name)
fill_review_table(cur, all_data, fields_and_types_dict, review_table_name)

con.close()
