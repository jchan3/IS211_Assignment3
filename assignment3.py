#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Docstring for Joe Chan: assignment2.py."""


import urllib2
import datetime
import argparse
import csv
import re


def downloadData(urlstr):
    """Open and read a CSV file found at a website URL and return a string.

    Args:
        urlstr(string): The website whose data will be read and interpreted.

    Returns:
        string: A string containing the CSV data.
    """
    try:
        response = urllib2.urlopen(urlstr)
        reader = csv.reader(response)
    except urllib2.HTTPError as e:
        print "The server could not fulfill the request."
        print "Error code: ", e.code
    except urllib2.URLError as e:
        print "We failed to reach a server."
        print "Reason: ", e.reason
    else:
        return reader


def processData(csv_data):
    """Takes the contents of the file, processes the file line by line, and
        returns a list of lists of the files, datatimes, browsers, status, and
        bytesizes of every line.

    Args:
        urldata(string): The data in the CSV file to be read.

    Returns:
        list: A list of 5 lists.
    """
    format_dt = "%Y-%m-%d %H:%M:%S"
    filelist = []
    datelist = []
    browserlist = []
    statuslist = []
    bytesizelist = []

    for line in csv_data:
        path_to_file = line[0]
        filelist.append(path_to_file)
        dt = datetime.datetime.strptime(line[1], format_dt)
        browser = line[2]
        status = line[3]
        byte_size = line[4]
        datelist.append(dt)
        browserlist.append(browser)
        statuslist.append(status)
        bytesizelist.append(byte_size)

    masterlist = [filelist, datelist, browserlist, statuslist, bytesizelist]
    return masterlist


def image_hits(files):
    """Searches for all hits of an image file using regular expressions.

    Args:
        files(list): A list of the files requested.
    """
    img_re = r"(\.png|\.PNG|\.JPG|\.jpg|\.GIF|\.gif)$"
    hit_count = 0
    total_count = len(files)

    for line in files:
        if re.search(img_re, line):
            hit_count += 1

    #print "hit count is: ", str(hit_count)
    #print "total count is: ", str(total_count)
    img_pct = round(((float(hit_count) / total_count)*100), 1)
    print "Image requests account for", str(img_pct) + "% of all requests."
    return


def browser_hits(browsers):
    """Searches and counts for all the browsers using regular expressions.
        The browsers are Firefox, Chrome, MSIE, or Safari.

    Args:
        browsers(list): A list of the browsers used.
    """
    ff_re = r"\sFirefox/"
    ie_re = r"\sMSIE\s"
    chrome_re = r"\sChrome/"
    safari_re = r"\sSafari/"
    ff_count = 0
    chrome_count = 0
    ie_count = 0
    safari_count = 0

    for line in browsers:
        if re.search(ff_re, line):
            ff_count += 1
        elif re.search(ie_re, line):
            ie_count += 1
        elif re.search(chrome_re, line):
            chrome_count += 1
        elif re.search(safari_re, line):
            safari_count += 1
        else:
            print "browser not found"

    #print "Firefox hits are: ", ff_count
    #print "MSIE hits are: ", ie_count
    #print "Chrome hits are: ", chrome_count
    #print "Safari hits are: ", safari_count

    if (ff_count > ie_count and ff_count > chrome_count and
            ff_count > safari_count):
        print "Firefox is the most popular browser on this day."
    elif (ie_count > ff_count and ie_count > chrome_count and ie_count >
          safari_count):
        print "Internet Explorer is the most popular browser on this day."
    elif (chrome_count > ff_count and chrome_count > ie_count and chrome_count >
          safari_count):
        print "Chrome is the most popular browser on this day."
    elif (safari_count > ff_count and safari_count > ie_count and safari_count >
          safari_count > chrome_count):
        print "Safari is the most popular browser on this day."

    return


def hour_hits(datetimes):
    """Outputs a list of hours of the day sorted by the total number of hits
        that occurred in that hour.

    Args:
        datetimes(list): A list of the datetime hits.
    """
    hits = 1
    temphour1 = datetimes[0].strftime("%H")

    for line in datetimes[1:]:
        temphour2 = line.strftime("%H")
        if temphour1 != temphour2:
            print "Hour", temphour1 + " has", str(hits) + " hits"
            temphour1 = temphour2
            hits = 1
        else:
            hits += 1
        if line == datetimes[-1]:
            print "Hour", temphour2 + " has", str(hits) + " hits"

    return


if __name__ == "__main__":
    #url = "http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv"

    parser = argparse.ArgumentParser(description="Enter URL address")
    parser.add_argument("url", help="Enter the URL address of the file")
    args = parser.parse_args()

    if args.url:
        url = args.url
        csvData = downloadData(url)
        file_Data = processData(csvData)
        image_hits(file_Data[0])
        browser_hits(file_Data[2])
        hour_hits(file_Data[1])
