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
    print args
except SystemExit:
    parser.print_help()
    sys.exit()

def get_JSON_data(filepath, key, prev_data={}):
    with open(filepath) as f:
        prev_data[key] = []
        for line in f:
            prev_data[key].append(line)
    return prev_data

all_data = {}
all_data = get_JSON_data(args.business, "business", prev_data=all_data)
all_data = get_JSON_data(args.checkin, "checkin", prev_data=all_data)
all_data = get_JSON_data(args.review, "review", prev_data=all_data)
all_data = get_JSON_data(args.user, "user", prev_data=all_data)
print all_data.keys()
