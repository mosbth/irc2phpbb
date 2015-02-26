#! /usr/bin/env python
# -*- coding: utf-8 -*-

""" 
Module that can be used to get a string containing a really short
description of a function in PHP. It pareses the PHP manual website to
get the information. 

It was created to be used with the irc bot marvin:
https://github.com/mosbth/irc2phpbb

Created by Andreas 'thebiffman' Andersson (andreas@biffnet.se)
"""

import urllib2
from bs4 import BeautifulSoup, SoupStrainer
import os

# Used to create the complete URL
BASE_URL = 'http://php.net/manual/en/function.'
ENDING_URL = '.php'

# File used to cache the function description strings
CACHE_FILE = 'phpmanual_cache.txt'


def cacheLookup(function):
    """
    If the function description is cached in the file, the function 
    returns it, otherwise it returns None.
    """
    if os.path.isfile(CACHE_FILE):
        try:
            cacheFile = open(CACHE_FILE, 'r')
            for line in cacheFile:
                endPos = line.index("http://p")
                if function in line[12:endPos]:
                    return line.rstrip('\n')
            cacheFile.close()
        except:
            return None
    return None


def saveToCache(description):
    """ 
    Appends the cache file with the prepared string that cotains 
    the function description.
    """
    cacheFile = open(CACHE_FILE, 'a')
    #print('Saving the following to cache:') DEBUG
    #print(description + '\n') DEBUG
    cacheFile.write(description + '\n')
    cacheFile.close()


def getShortDescr(function):
    """ 
    Uses the given function name and attemps to get a short description 
    from the php manual. Returns a string with "Nothing found" if nothing 
    was found, or a pretty string with the information requested. 
    """

    # If the function description is cached, return it
    cached = cacheLookup(function)
    if(cached is not None):
        return cached

    # Replace '_' with '-'
    function = function.replace('_', '-')

    # Complete URL to the manual page (if it exists)
    url = BASE_URL+function+ENDING_URL

    # Try to fetch the site. If a incorrect function name is 
    # used, this will fail and print an error code. 
    siteData = None
    try:
        #print('Start to read') DEBUG
        siteData = urllib2.urlopen(url)
        #print('Done reading.') DEBUG
    except urllib2.HTTPError, e:
        print(e.code)
    except urllib2.URLError, e:
        print(e.args)

    # This is the default value that will be returned if nothing is found.
    result = 'Found nothing.'

    # Actually parse and find the text 
    if siteData is not None:
        # Use SoupStrainer to only parse what I need
        tagsWithClass = SoupStrainer('p',{'class': 'refpurpose'})

        #print('Done creating SoupStrainer.') DEBUG

        # Create the soup object, using the SoupStrainer.
        # This is what takes the most time (hence the .txt-file cache)
        soup = BeautifulSoup(siteData, "lxml",  parse_only=tagsWithClass)

        #print('Done creating BeautifulSoup.') DEBUG

        # Get the specific tag I need
        shortDescrPtag = soup.find("p", { "class" : "refpurpose" })

        #print('Done finding tag.') DEBUG
        try:
            # Put the text without html tags in my fancy string
            result = 'PHP-manualen: ' + shortDescrPtag.get_text() + ' - ' + url
            result = result.replace('\n', '')
            result = result.encode('utf-8')
            # Cache the result (i.e. save it to the cache txt-file)
            saveToCache(result)
        except:
            result = 'Found nothing.'

    # Return the result
    return result

# Used for testing
#print(getShortDescr('substr'))
