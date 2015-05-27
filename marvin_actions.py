#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make actions for Marvin, one function for each action.
"""


import random
import json
from datetime import date
import feedparser
from bs4 import BeautifulSoup
from urllib.request import urlopen


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
        marvinStrip
    ]


# Load all strings from file
with open("marvin_strings.json") as f:
    STRINGS = json.load(f)


def getString(key, key1=None):
    """
    Get a string from the string database.
    """
    data = STRINGS[key]
    if type(data) is list:
        res = data[random.randint(0, len(data) - 1)]
    elif type(data) is dict:
        res = data[key1]
    elif type(data) is str:
        res = data

    return res


def marvinSmile(line, row):
    """
    Make Marvin smile.
    """
    msg = None
    if row.intersection(['smile', 'le', 'skratta', 'smilies']):
        smilie = getString("smile")
        msg = "{SMILE}".format(SMILE=smilie)
    return msg


def marvinSource(line, row):
    """
    State message about sourcecode.
    """
    msg = None
    if row.intersection(['källkod', 'source']):
        msg = getString("source")

    return msg


def marvinBudord(line, row):
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


def marvinQuote(line, row):
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
    dayNum = date.weekday(date.today()) + 1
    msg = getString("weekdays", str(dayNum))
    video = getString("video-of-today", str(dayNum))

    if video:
        msg += " En passande video är " + video
    else:
        msg += " Jag har ännu ingen passande video för denna dagen."

    return msg


def marvinVideoOfToday(line, row):
    """
    Show the video of today.
    """
    msg = None
    if row.intersection(['idag', 'dagens']) and row.intersection(['video', 'youtube', 'tube']):
        msg = videoOfToday()

    return msg


def marvinWhoIs(line, row):
    """
    Who is Marvin.
    """
    msg = None
    if row.issuperset(['vem', 'är']):
        msg = getString("whois")

    return msg


def marvinHelp(line, row):
    """
    Provide a menu.
    """
    msg = None
    if row.intersection(['hjälp', 'help', 'menu', 'meny']):
        msg = getString("menu")

    return msg


def marvinStats(line, row):
    """
    Provide a link to the stats.
    """
    msg = None
    if row.intersection(['stats', 'statistik', 'ircstats']):
        msg = getString("ircstats")

    return msg


def marvinSayHi(line, row):
    """
    Say hi with a nice message.
    """
    msg = None
    if row.intersection(['snälla', 'hej', 'tjena', 'morsning', 'mår', 'hallå', 'halloj', 'läget', 'snäll', 'duktig', 'träna', 'träning', 'utbildning', 'tack', 'tacka', 'tackar', 'tacksam']):
        smile = getString("smile")
        hello = getString("hello")
        friendly = getString("friendly")
        msg = "{} {} {}".format(smile, hello, friendly)

    return msg


def marvinLunch(line, row):
    """
    Help decide where to eat.
    """
    msg = None
    if row.intersection(['lunch', 'mat', 'äta']):
        if row.intersection(['stan', 'centrum', 'karlskrona', 'kna']):
            msg = getString("lunch-message").format(getString("lunch-karlskrona"))
        elif row.intersection(['hässleholm', 'hassleholm']):
            msg = getString("lunch-message").format(getString("lunch-hassleholm"))
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


def marvinListen(line, row):
    """
    Return music last listened to.
    """
    msg = None
    if row.intersection(['lyssna', 'lyssnar', 'musik']):
        feed = feedparser.parse('http://ws.audioscrobbler.com/1.0/user/mikaelroos/recenttracks.rss')
        # feed["items"][0]["title"].encode('utf-8', 'ignore')))
        msg = getString("listen") + " " + feed["items"][0]["title"]

    return msg


def marvinSun(line, row):
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

        except Exception as e:
            msg = getString("sun-no")

    return msg


def marvinWeather(line, row):
    """
    Check what the weather prognosis looks like.
    """
    msg = None
    if row.intersection(['väder', 'vädret', 'prognos', 'prognosen', 'smhi']):
        soup = BeautifulSoup(urlopen('http://www.smhi.se/vadret/vadret-i-sverige/Vaderoversikt-Sverige-meteorologens-kommentar?meteorologens-kommentar=http%3A%2F%2Fwww.smhi.se%2FweatherSMHI2%2Flandvader%2F.%2Fprognos15_2.htm'))
        msg = "{}. {}. {}".format(soup.h1.text, soup.h4.text, soup.h4.findNextSibling('p').text)

    return msg


def marvinStrip(line, row):
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


"""
      elif ('latest' in row or 'senaste' in row or 'senast' in row) and ('forum' in row or 'forumet' in row):
        feed=feedparser.parse(FEED_FORUM)
        sendPrivMsg(s,"Forumet: \"%s\" av %s http://dbwebb.se/f/%s" % (feed["items"][0]["title"].encode('utf-8', 'ignore'), feed["items"][0]["author"].encode('utf-8', 'ignore'), re.search('(?<=p=)\d+', feed["items"][0]["id"].encode('utf-8', 'ignore')).group(0)))
"""
