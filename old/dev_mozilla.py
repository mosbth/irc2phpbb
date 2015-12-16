#! /usr/bin/env python
# -*- coding: utf-8 -*-

""" 
Module that can be used to get a string containing a short description 
from the first search result on 'developer.mozilla.org'. It also adds 
the URL to the details page.

Right now it is only made with JavaScript in mind, but searching
in other categories can easily be added later. 

It was created to be used with the irc bot marvin:
https://github.com/mosbth/irc2phpbb

Created by Andreas 'thebiffman' Andersson (andreas@biffnet.se)
"""

import urllib2
from bs4 import BeautifulSoup, SoupStrainer
import os

# Used to create the complete URL
BASE_URL = 'https://developer.mozilla.org/en-US/search?q='
URL_TOPIC_JS = '&topic=api&topic=js'


def getResultString(function, filter='js'):
    """ 
    Uses the given function name and searches for it on the mozilla
    developer network. Returns a string with "Nothing found" if nothing 
    was found, or a pretty string with the information requested along
    with a link.
    """

    # Asemble the basic search url
    url = BASE_URL+function

    #print("Url: " + url)

    if 'js' in filter or 'javascript' in filter:
        url = url + URL_TOPIC_JS

    #print("Url: " + url)

    # Try to fetch the site. If a incorrect function name is 
    # used, this will fail and print an error code. 
    siteData = None
    try:
        #print('Start to read')
        siteData = urllib2.urlopen(url)
        #print('Done reading.')
    except urllib2.HTTPError, e:
        print(e.code)
    except urllib2.URLError, e:
        print(e.args)

    # This is the default value that will be returned if nothing is found.
    result = 'Found nothing.'

    # Actually parse and find the text 
    if siteData is not None:

        # Use SoupStrainer to only parse what I need
        strainer = SoupStrainer('li',{'class': 'result-1'})

        # Create the soup object, using the SoupStrainer.
        soup = BeautifulSoup(siteData, "lxml",  parse_only=strainer)

        # Get all a tags
        linkTags = soup.find_all("a")
        descriptionTag = soup.find("p")

        if len(linkTags) < 2:
            return result

        # Trying to check that fields arent empty or contain too strange data
        #if len(linkTags[0].get_text()) < 4 or len(linkTags[1].get_text()) < 21 or len(descriptionTag.get_text()) < 15:
        #    return result

        # First a tag is the title/name of the result
        resultName = linkTags[0].get_text()

        # Second a tag is the url of the result
        resultLink = 'https://' + linkTags[1].get_text()

        # The P tag contains the description
        resultDescription = descriptionTag.get_text().rstrip()

        # Put the text without html tags in my fancy string
        result = 'MDN: ' + resultName + ' - ' + resultDescription + ' - ' + resultLink

        result = result.encode('utf-8')

        #print(result)

    # Return the result
    return result

# Used for testing
#print(getResultString('getElementById'))
