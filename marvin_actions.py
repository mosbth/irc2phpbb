#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make actions for Marvin, one function for each action.
"""


import random
import math
import json
import datetime
from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

# Used or not?
#import feedparser


def getAllActions():
    """
    Return all actions in an array.
    """
    return [
        marvinLunch,
        marvinVideoOfToday,
        marvinWhoIs,
        marvinHelp,
        marvinSource,
        marvinBudord,
        marvinQuote,
        marvinStats,
        marvinListen,
        marvinWeather,
        marvinSun,
        marvinSayHi,
        marvinSmile,
        marvinStrip,
        marvinGoogle,
        marvinTimeToBBQ
    ]


# Load all strings from file
with open("marvin_strings.json") as f:
    STRINGS = json.load(f)


def getString(key, key1=None):
    """
    Get a string from the string database.
    """
    data = STRINGS[key]
    if isinstance(data, list):
        res = data[random.randint(0, len(data) - 1)]
    elif isinstance(data, dict):
        res = data[key1]
    elif isinstance(data, str):
        res = data

    return res


def marvinSmile(row, asList=None, asStr=None):
    """
    Make Marvin smile.
    """
    msg = None
    if row.intersection(['smile', 'le', 'skratta', 'smilies']):
        smilie = getString("smile")
        msg = "{SMILE}".format(SMILE=smilie)
    return msg


def generateUrlToGoogleSearch(searchStr):
    """
    Generates an google query-url based input string
    """
    baseUrl = 'https://www.google.se/search?q='
    searchFor = quote_plus(searchStr)

    return baseUrl + searchFor


def marvinGoogle(row, asList=None, asStr=None):
    """
    Let Marvin present an url to google.
    """
    msg = None
    match = row.intersection(['google', 'googla'])

    if match:
        # Find the google word and take the rest as the query string
        startAt = next(iter(match))
        searchStart = asList.index(startAt) + 1

        if searchStart >= len(asList):
            searchStr = ""
        else:
            searchStr = " ".join(asList[searchStart:])
        
        url = generateUrlToGoogleSearch(searchStr)
        google = getString("google")
        msg = google.format(url)

    return msg


def marvinSource(row, asList=None, asStr=None):
    """
    State message about sourcecode.
    """
    msg = None
    if row.intersection(['källkod', 'source']):
        msg = getString("source")

    return msg


def marvinBudord(row, asList=None, asStr=None):
    """
    What are the budord for Marvin?
    """
    msg = None
    if row.intersection(['budord', 'stentavla']):
        if row.intersection(['1', '#1']):
            msg = getString("budord", "#1")
        elif row.intersection(['2', '#2']):
            msg = getString("budord", "#2")
        elif row.intersection(['3', '#3']):
            msg = getString("budord", "#3")
        elif row.intersection(['4', '#4']):
            msg = getString("budord", "#4")
        elif row.intersection(['5', '#5']):
            msg = getString("budord", "#5")

    return msg


def marvinQuote(row, asList=None, asStr=None):
    """
    Make a quote.
    """
    msg = None
    if row.intersection(['quote', 'citat', 'filosofi', 'filosofera']):
        msg = getString("hitchhiker")

    return msg


def videoOfToday():
    """
    Check what day it is and provide a url to a suitable video together with a greeting.
    """
    dayNum = datetime.date.weekday(datetime.date.today()) + 1
    msg = getString("weekdays", str(dayNum))
    video = getString("video-of-today", str(dayNum))

    if video:
        msg += " En passande video är " + video
    else:
        msg += " Jag har ännu ingen passande video för denna dagen."

    return msg


def marvinVideoOfToday(row, asList=None, asStr=None):
    """
    Show the video of today.
    """
    msg = None
    if row.intersection(['idag', 'dagens']) and row.intersection(['video', 'youtube', 'tube']):
        msg = videoOfToday()

    return msg


def marvinWhoIs(row, asList=None, asStr=None):
    """
    Who is Marvin.
    """
    msg = None
    if row.issuperset(['vem', 'är']):
        msg = getString("whois")

    return msg


def marvinHelp(row, asList=None, asStr=None):
    """
    Provide a menu.
    """
    msg = None
    if row.intersection(['hjälp', 'help', 'menu', 'meny']):
        msg = getString("menu")

    return msg


def marvinStats(row, asList=None, asStr=None):
    """
    Provide a link to the stats.
    """
    msg = None
    if row.intersection(['stats', 'statistik', 'ircstats']):
        msg = getString("ircstats")

    return msg


def marvinSayHi(row, asList=None, asStr=None):
    """
    Say hi with a nice message.
    """
    msg = None
    if row.intersection([
            'snälla', 'hej', 'tjena', 'morsning', 'mår', 'hallå', 'halloj',
            'läget', 'snäll', 'duktig', 'träna', 'träning', 'utbildning',
            'tack', 'tacka', 'tackar', 'tacksam'
    ]):
        smile = getString("smile")
        hello = getString("hello")
        friendly = getString("friendly")
        msg = "{} {} {}".format(smile, hello, friendly)

    return msg


def marvinLunch(row, asList=None, asStr=None):
    """
    Help decide where to eat.
    """
    msg = None
    if row.intersection(['lunch', 'mat', 'äta']):
        if row.intersection(['stan', 'centrum', 'karlskrona', 'kna']):
            msg = getString("lunch-message").format(getString("lunch-karlskrona"))
        elif row.intersection(['ängelholm', 'angelholm', 'engelholm']):
            msg = getString('lunch-message').format(getString('lunch-angelholm'))
        elif row.intersection(['hässleholm', 'hassleholm']):
            msg = getString("lunch-message").format(getString("lunch-hassleholm"))
        elif row.intersection(['malmö', 'malmo', 'malmoe']):
            msg = getString("lunch-message").format(getString("lunch-malmo"))
        else:
            msg = getString("lunch-message").format(getString("lunch-bth"))

    return msg


def getListen():
    """
    Nice message about listening to a song.
    """
    data = [
        'Jag gillar låten',
        'Senaste låten jag lyssnade på var',
        'Jag lyssnar just nu på',
        'Har du hört denna låten :)',
        'Jag kan tipsa om en bra låt ->'
    ]
    res = data[random.randint(0, len(data) - 1)]
    return res


def marvinListen(row, asList=None, asStr=None):
    """
    Return music last listened to.
    """
    msg = None
    if row.intersection(['lyssna', 'lyssnar', 'musik']):
        msg = "Jag lyssnar inte på något för tillfället..."
        #feed = feedparser.parse('http://ws.audioscrobbler.com/1.0/user/mikaelroos/recenttracks.rss')
        # feed["items"][0]["title"].encode('utf-8', 'ignore')))
        #msg = getString("listen") + " " + feed["items"][0]["title"]

    return msg


def marvinSun(row, asList=None, asStr=None):
    """
    Check when the sun goes up and down.
    """
    msg = None
    if row.intersection(['sol', 'solen', 'solnedgång', 'soluppgång']):
        try:
            soup = BeautifulSoup(urlopen('http://www.timeanddate.com/sun/sweden/jonkoping'))
            spans = soup.find_all("span", {"class": "three"})
            sunrise = spans[0].text
            sunset = spans[1].text
            msg = getString("sun").format(sunrise, sunset)

        except Exception:
            msg = getString("sun-no")

    return msg


def marvinWeather(row, asList=None, asStr=None):
    """
    Check what the weather prognosis looks like.
    """
    msg = None
    if row.intersection(["väder", "vädret", "prognos", "prognosen", "smhi"]):
        url = getString("smhi", "url")
        try:
            soup = BeautifulSoup(urlopen(url))
            msg = "{}. {}. {}".format(
                soup.h1.text,
                soup.h4.text,
                soup.h4.findNextSibling("p").text
            )

        except Exception:
            msg = getString("smhi", "failed")

    return msg


def marvinStrip(row, asList=None, asStr=None):
    """
    Get a comic strip.
    """
    msg = None
    if row.intersection(['strip', 'comic']):
        if row.intersection(['rand', 'random', 'slump', 'lucky']):
            msg = commitStrip(randomize=True)
        else:
            msg = commitStrip()

    return msg


def commitStrip(randomize=False):
    """
    Latest or random comic strip from CommitStrip.
    """
    msg = getString("commitstrip", "message")

    if randomize:
        first = getString("commitstrip", "first")
        last = getString("commitstrip", "last")
        rand = random.randint(first, last)
        url = getString("commitstrip", "urlPage") + str(rand)
    else:
        url = getString("commitstrip", "url")

    return msg.format(url=url)


#      elif ('latest' in row or 'senaste' in row or 'senast' in row)
# and ('forum' in row or 'forumet' in row):
#        feed=feedparser.parse(FEED_FORUM)


def marvinTimeToBBQ(row, asList=None, asStr=None):
    """
    Calcuate the time to next barbecue and print a appropriate msg
    """
    msg = None
    if row.intersection(['grilla', 'grill', 'bbq']):
        whenStr = getString("barbecue", "when")
        whenDate = datetime.datetime.strptime(whenStr, '%Y-%m-%d')
        now = datetime.datetime.now()
        days = math.floor((whenDate - now) / datetime.timedelta(hours=24))

        if (days == -1):
            msg = getString("barbecue", "today")
        elif (days == 0):
            msg = getString("barbecue", "tomorrow")
        elif (days < 14 and days > 0):
            part = getString("barbecue", "week")
            msg = getRandomAnswerForBBQ(part, whenStr)
        elif (days < 200 and days > 0):
            part = getString("barbecue", "base")
            msg = getRandomAnswerForBBQ(part, whenStr)
        else:
            msg = getString("barbecue", "eternity")

        return msg

def getRandomAnswerForBBQ(part, whenStr):
    """
    Generates a random string from the part-array given
    """
    rand = random.randint(0, len(part) - 1)
    msg = ""
    try:
        msg = part[rand] % whenStr
    except TypeError:
        msg = part[rand]

    return msg
