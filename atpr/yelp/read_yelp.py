#!/usr/bin/python
import json
import matplotlib.pyplot as plot
import sys
import argparse

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

all_data = {}
all_data = get_JSON_data(args.business, "business", sub_key="business_id" ,prev_data=all_data)
all_data = get_JSON_data(args.checkin, "checkin", sub_key="business_id", prev_data=all_data)
all_data = get_JSON_data(args.review, "review", sub_key="business_id", prev_data=all_data)
all_data = get_JSON_data(args.user, "user", sub_key="user_id", prev_data=all_data)
print "Loaded all datasets"

all_business_ids = all_data["business"].keys()
print all_data["business"][all_business_ids[0]]
print all_data["checkin"][all_business_ids[0]]
print all_data["review"][all_business_ids[0]]
