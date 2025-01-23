#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make actions for Marvin, one function for each action.
"""
from urllib.parse import quote_plus
from urllib.request import urlopen
import calendar
import datetime
import json
import logging
import random
import requests

from bs4 import BeautifulSoup

LOG = logging.getLogger("action")

def getAllActions():
    """
    Return all actions in an array.
    """
    return [
        marvinExplainShell,
        marvinGoogle,
        marvinLunch,
        marvinVideoOfToday,
        marvinWhoIs,
        marvinHelp,
        marvinSource,
        marvinBudord,
        marvinQuote,
        marvinWeather,
        marvinSun,
        marvinSayHi,
        marvinSmile,
        marvinStrip,
        marvinTimeToBBQ,
        marvinBirthday,
        marvinNameday,
        marvinUptime,
        marvinStream,
        marvinPrinciple,
        marvinJoke,
        marvinCommit
    ]


# Load all strings from file
with open("marvin_strings.json", encoding="utf-8") as f:
    STRINGS = json.load(f)


def getString(key, key1=None):
    """
    Get a string from the string database.
    """
    data = STRINGS[key]
    if isinstance(data, list):
        res = data[random.randint(0, len(data) - 1)]
    elif isinstance(data, dict):
        if key1 is None:
            res = data
        else:
            res = data[key1]
            if isinstance(res, list):
                res = res[random.randint(0, len(res) - 1)]
    elif isinstance(data, str):
        res = data

    return res


def marvinSmile(row):
    """
    Make Marvin smile.
    """
    msg = None
    if any(r in row for r in ["smile", "le", "skratta", "smilies"]):
        msg = getString("smile")
    return msg


def wordsAfterKeyWords(words, keyWords):
    """
    Return all items in the words list after the first occurence
    of an item in the keyWords list.
    """
    kwIndex = []
    for kw in keyWords:
        if kw in words:
            kwIndex.append(words.index(kw))

    if not kwIndex:
        return None

    return words[min(kwIndex)+1:]


def marvinGoogle(row):
    """
    Let Marvin present an url to google.
    """
    query = wordsAfterKeyWords(row, ["google", "googla"])
    if not query:
        return None

    searchStr = " ".join(query)
    url = "https://www.google.se/search?q="
    url += quote_plus(searchStr)
    msg = getString("google")
    return msg.format(url)


def marvinExplainShell(row):
    """
    Let Marvin present an url to the service explain shell to
    explain a shell command.
    """
    query = wordsAfterKeyWords(row, ["explain", "förklara"])
    if not query:
        return None
    cmd = " ".join(query)
    url = "https://explainshell.com/explain?cmd="
    url += quote_plus(cmd, "/:")
    msg = getString("explainShell")
    return msg.format(url)


def marvinSource(row):
    """
    State message about sourcecode.
    """
    msg = None
    if any(r in row for r in ["källkod", "source"]):
        msg = getString("source")

    return msg


def marvinBudord(row):
    """
    What are the budord for Marvin?
    """
    msg = None
    if any(r in row for r in ["budord", "stentavla"]):
        if any(r in row for r in ["#1", "1"]):
            msg = getString("budord", "#1")
        elif any(r in row for r in ["#2", "2"]):
            msg = getString("budord", "#2")
        elif any(r in row for r in ["#3", "3"]):
            msg = getString("budord", "#3")
        elif any(r in row for r in ["#4", "4"]):
            msg = getString("budord", "#4")
        elif any(r in row for r in ["#5", "5"]):
            msg = getString("budord", "#5")

    return msg


def marvinQuote(row):
    """
    Make a quote.
    """
    msg = None
    if any(r in row for r in ["quote", "citat", "filosofi", "filosofera"]):
        msg = getString("hitchhiker")

    return msg


def videoOfToday():
    """
    Check what day it is and provide a url to a suitable video together with a greeting.
    """
    weekday = datetime.date.today().strftime("%A")
    day = getString("video-of-today", weekday)
    msg = day.get("message")

    if day:
        msg += " En passande video är " + day.get("url")
    else:
        msg += " Jag har ännu ingen passande video för denna dagen."

    return msg


def marvinVideoOfToday(row):
    """
    Show the video of today.
    """
    msg = None
    if any(r in row for r in ["idag", "dagens"]):
        if any(r in row for r in ["video", "youtube", "tube"]):
            msg = videoOfToday()

    return msg


def marvinWhoIs(row):
    """
    Who is Marvin.
    """
    msg = None
    if all(r in row for r in ["vem", "är"]):
        msg = getString("whois")

    return msg


def marvinHelp(row):
    """
    Provide a menu.
    """
    msg = None
    if any(r in row for r in ["hjälp", "help", "menu", "meny"]):
        msg = getString("menu")

    return msg


def marvinSayHi(row):
    """
    Say hi with a nice message.
    """
    msg = None
    if any(r in row for r in [
            "snälla", "hej", "tjena", "morsning", "morrn", "mår", "hallå",
            "halloj", "läget", "snäll", "duktig", "träna", "träning",
            "utbildning", "tack", "tacka", "tackar", "tacksam"
    ]):
        smile = getString("smile")
        hello = getString("hello")
        friendly = getString("friendly")
        msg = f"{smile} {hello} {friendly}"

    return msg


def marvinLunch(row):
    """
    Help decide where to eat.
    """
    lunchOptions = {
        'stan centrum karlskrona kna': 'karlskrona',
        'ängelholm angelholm engelholm': 'angelholm',
        'hässleholm hassleholm': 'hassleholm',
        'malmö malmo malmoe': 'malmo',
        'göteborg goteborg gbg': 'goteborg'
    }

    data = getString("lunch")

    if any(r in row for r in ["lunch", "mat", "äta", "luncha"]):
        places = data.get("location").get("bth")
        for keys, value in lunchOptions.items():
            if any(r in row for r in keys.split(" ")):
                places = data.get("location").get(value)

        lunchStr = getString("lunch", "message")
        return lunchStr.format(places[random.randint(0, len(places) - 1)])

    return None


def marvinSun(row):
    """
    Check when the sun goes up and down.
    """
    msg = None
    if any(r in row for r in ["sol", "solen", "solnedgång", "soluppgång", "sun"]):
        try:
            url = getString("sun", "url")
            r = requests.get(url, timeout=5)
            sundata = r.json()
            # Formats the time from the response to HH:mm instead of hh:mm:ss
            sunrise = sundata["results"]["sunrise"].split()[0][:-3]
            sunset = sundata["results"]["sunset"].split()[0][:-3]
            # The api uses AM/PM notation, this converts the sunset to 12 hour time
            sunsetHour = int(sunset.split(":")[0]) + 12
            sunset = str(sunsetHour) + sunset[-3:]
            msg = getString("sun", "msg").format(sunrise, sunset)
            return msg

        except Exception as e:
            LOG.error("Failed to get sun times: %s", e)
            return getString("sun", "error")

    return msg


def marvinWeather(row):
    """
    Check what the weather prognosis looks like.
    """
    msg = ""
    if any(r in row for r in ["väder", "vädret", "prognos", "prognosen", "smhi"]):
        forecast = ""
        observation = ""

        try:
            station_req = requests.get(getString("smhi", "station_url"), timeout=5)
            weather_code:int = int(station_req.json().get("value")[0].get("value"))

            weather_codes_req = requests.get(getString("smhi", "weather_codes_url"), timeout=5)
            weather_codes_arr: list = weather_codes_req.json().get("entry")

            current_weather_req = requests.get(getString("smhi", "current_weather_url"), timeout=5)
            current_w_data: list = current_weather_req.json().get("timeSeries")[0].get("parameters")

            for curr_w in current_w_data:
                if curr_w.get("name") == "t":
                    forecast = curr_w.get("values")[0]

            for code in weather_codes_arr:
                if code.get("key") == weather_code:
                    observation = code.get("value")

            msg = f"Karlskrona just nu: {forecast} °C. {observation}."

        except Exception as e:
            LOG.error("Failed to get weather: %s", e)
            msg: str = getString("smhi", "failed")

    return msg


def marvinStrip(row):
    """
    Get a comic strip.
    """
    msg = None
    if any(r in row for r in ["strip", "comic", "nöje", "paus"]):
        msg = commitStrip(randomize=any(r in row for r in ["rand", "random", "slump", "lucky"]))
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


def marvinTimeToBBQ(row):
    """
    Calcuate the time to next barbecue and print a appropriate msg
    """
    msg = None
    if any(r in row for r in ["grilla", "grill", "grillcon", "bbq"]):
        url = getString("barbecue", "url")
        nextDate = nextBBQ()
        today = datetime.date.today()
        daysRemaining = (nextDate - today).days

        if daysRemaining == 0:
            msg = getString("barbecue", "today")
        elif daysRemaining == 1:
            msg = getString("barbecue", "tomorrow")
        elif 1 < daysRemaining < 14:
            msg = getString("barbecue", "week") % nextDate
        elif 14 < daysRemaining < 200:
            msg = getString("barbecue", "base") % nextDate
        else:
            msg = getString("barbecue", "eternity") % nextDate

        msg = url + ". " + msg
    return msg

def nextBBQ():
    """
    Calculate the next grillcon date after today
    """

    MAY = 5
    SEPTEMBER = 9

    after = datetime.date.today()
    spring = thirdFridayIn(after.year, MAY)
    if after <= spring:
        return spring

    autumn = thirdFridayIn(after.year, SEPTEMBER)
    if after <= autumn:
        return autumn

    return thirdFridayIn(after.year + 1, MAY)


def thirdFridayIn(y, m):
    """
    Get the third Friday in a given month and year
    """
    THIRD = 2
    FRIDAY = -1

    # Start the weeks on saturday to prevent fridays from previous month
    cal = calendar.Calendar(firstweekday=calendar.SATURDAY)

    # Return the friday in the third week
    return cal.monthdatescalendar(y, m)[THIRD][FRIDAY]


def marvinBirthday(row):
    """
    Check birthday info
    """
    msg = None
    if any(r in row for r in ["birthday", "födelsedag"]):
        try:
            url = getString("birthday", "url")
            soup = BeautifulSoup(urlopen(url), "html.parser")
            my_list = list()

            for ana in soup.findAll('a'):
                if ana.parent.name == 'strong':
                    my_list.append(ana.getText())

            my_list.pop()
            my_strings = ', '.join(my_list)
            if not my_strings:
                msg = getString("birthday", "nobody")
            else:
                msg = getString("birthday", "somebody").format(my_strings)

        except Exception as e:
            LOG.error("Failed to get birthday: %s", e)
            msg = getString("birthday", "error")

    return msg

def marvinNameday(row):
    """
    Check current nameday
    """
    msg = None
    if any(r in row for r in ["nameday", "namnsdag"]):
        try:
            now = datetime.datetime.now()
            raw_url = "https://api.dryg.net/dagar/v2.1/{year}/{month}/{day}"
            url = raw_url.format(year=now.year, month=now.month, day=now.day)
            r = requests.get(url, timeout=5)
            nameday_data = r.json()
            names = nameday_data["dagar"][0]["namnsdag"]
            parsed_names = formatNames(names)
            if names:
                msg = getString("nameday", "somebody").format(parsed_names)
            else:
                msg = getString("nameday", "nobody")
        except Exception as e:
            LOG.error("Failed to get nameday: %s", e)
            msg = getString("nameday", "error")
    return msg

def formatNames(names):
    """
    Parses namedata from nameday API
    """
    if len(names) > 1:
        return " och ".join([", ".join(names[:-1])] + names[-1:])
    return "".join(names)

def marvinUptime(row):
    """
    Display info about uptime tournament
    """
    msg = None
    if "uptime" in row:
        msg = getString("uptime", "info")
    return msg

def marvinStream(row):
    """
    Display info about stream
    """
    msg = None
    if any(r in row for r in ["stream", "streama", "ström", "strömma"]):
        msg = getString("stream", "info")
    return msg

def marvinPrinciple(row):
    """
    Display one selected software principle, or provide one as random
    """
    msg = None
    if any(r in row for r in ["principle", "princip", "principer"]):
        principles = getString("principle")
        principleKeys = list(principles.keys())
        matchedKeys = [k for k in row if k in principleKeys]
        if matchedKeys:
            msg = principles[matchedKeys.pop()]
        else:
            msg = principles[random.choice(principleKeys)]
    return msg

def getJoke():
    """
    Retrieves joke from api.chucknorris.io/jokes/random?category=dev
    """
    try:
        url = getString("joke", "url")
        r = requests.get(url, timeout=5)
        joke_data = r.json()
        return joke_data["value"]
    except Exception as e:
        LOG.error("Failed to get joke: %s", e)
        return getString("joke", "error")

def marvinJoke(row):
    """
    Display a random Chuck Norris joke
    """
    msg = None
    if any(r in row for r in ["joke", "skämt", "chuck norris", "chuck", "norris"]):
        msg = getJoke()
    return msg

def getCommit():
    """
    Retrieves random commit message from whatthecommit.com/index.html
    """
    try:
        url = getString("commit", "url")
        r = requests.get(url, timeout=5)
        res = r.text.strip()
        msg = f"Använd detta meddelandet: '{res}'"
        return msg
    except Exception as e:
        LOG.error("Failed to get commit message: %s", e)
        return getString("commit", "error")

def marvinCommit(row):
    """
    Display a random commit message
    """
    msg = None
    if any(r in row for r in ["commit", "-m"]):
        msg = getCommit()
    return msg
