#!/usr/bin/env python3

import os
import time
import json
import requests
from collections import deque

DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
AP_API_KEY = os.environ['AP_API_KEY']
RATE_LIMIT_PER_MINUTE = 10

os.makedirs(f"{DATA_FOLDER}/raw_ap", exist_ok=True)

# http://www.thegreenpapers.com/G16/events.phtml?format=chronological
# http://customersupport.ap.org/doc/2016_Election_Calendar.pdf

# http://customersupport.ap.org/doc/2018_Election_Calendar.pdf
# http://www.thegreenpapers.com/G18/events.phtml?format=chronological

# query = "&level=state&officeID=S,H,G"
query = ""

dates = [
    
    "2012-11-06",
    "2014-11-04", # no results

    "2015-11-03",
    "2015-11-21",

    # February 2016
    "2016-02-01", "2016-02-09", "2016-02-16", "2016-02-20", "2016-02-23",
    "2016-02-27",

    # March 2016
    "2016-03-01", "2016-03-05", "2016-03-06", "2016-03-08", "2016-03-10",
    "2016-03-12", "2016-03-15", "2016-03-22", "2016-03-26",

    # April 2016
    "2016-04-05", "2016-04-09", "2016-04-12", "2016-04-16", "2016-04-19",
    "2016-04-26",

    # May 2016
    "2016-05-03", "2016-05-07", "2016-05-10", "2016-05-17", "2016-05-24",
    "2016-05-31",

    # June 2016
    "2016-06-04", "2016-06-05", "2016-06-07", "2016-06-14", "2016-06-21",
    "2016-06-28",

    # July 2016
    "2016-07-26",

    # August 2016
    "2016-08-02", "2016-08-04", "2016-08-09", "2016-08-13", "2016-08-16",
    "2016-08-23", "2016-08-30",

    # September 2016
    "2016-09-08", "2016-09-13",

    # November 2016
    "2016-11-08",

    # ----------------------------------------------------------------- #

    # February 2018
    "2018-02-27",

    # March 2018
    "2018-03-06", "2018-03-13", "2018-03-20",

    # April 2018
    "2018-04-24",

    # May 2018
    "2018-05-08", "2018-05-15", "2018-05-22",

    # June 2018
    "2018-06-05", "2018-06-12", "2018-06-19", "2018-06-26", "2018-06-30",

    # July 2018
    "2018-07-17", "2018-07-24",

    # August 2018
    "2018-08-02", "2018-08-07", "2018-08-11", "2018-08-14", "2018-08-21", "2018-08-28",

    # September 2018
    "2018-09-04", "2018-09-06", "2018-09-11", "2018-09-12", "2018-09-13",

    # Fake November 6
    "test-2018-11-06"

]

q = deque(reversed(dates))
counter = 0

start_time = time.time()

while q:
    date = q[-1]

    test = "false"
    if "test-" in date:
        date = date.replace('test-', '')
        test = "true"

    filepath = DATA_FOLDER + "/raw_ap/%s.json" % date
    if os.path.isfile(filepath):
        print("skipping %s because file already exists" % date)
        q.pop()
        continue

    if time.time() - start_time < 60 and counter >= 20:
        seconds_to_sleep = 60 - (time.time() - start_time)
        print("sleeping for %s" % seconds_to_sleep)
        time.sleep(seconds_to_sleep)
        start_time = time.time()
        counter = 0

    print("downloading %s" % date)
    response = requests.get(
        "https://api.ap.org/v2/elections/%s?test=%s&format=json%s"
        "&apikey=%s" % (date, test, query, AP_API_KEY))
    counter += 1
    if response.status_code == 403:
        print("hit rate limit!")
        continue
    data = response.json()
    if len(data['races']) == 0:
        q.pop()
        print("date %s had no races for selected filter" % date)
        time.sleep(0.5)
        continue

    with open(filepath, "w") as f:
        json.dump(data, f, indent=4, sort_keys=True)
    time.sleep(0.5)
    q.pop()
