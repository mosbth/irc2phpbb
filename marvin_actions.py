#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make actions for Marvin, one function for each action.
"""


import random
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
        marvinSmile
    ]


def getSmile():
    """
    Return a smile
    """
    data = [':-D', ':-P', ';-P', ';-)', ':-)', '8-)']
    res = data[random.randint(0, len(data) - 1)]
    return res


def getQuote():
    """
    Return a quote
    """
    data = [
        'I could calculate your chance of survival, but you won\'t like it.',
        'I\'d give you advice, but you wouldn\'t listen. No one ever does.',
        'I ache, therefore I am.',
        'I\'ve seen it. It\'s rubbish. (About a Magrathean sunset that Arthur finds magnificent)',
        'Not that anyone cares what I say, but the Restaurant is on the other end of the universe.',
        'I think you ought to know I\'m feeling very depressed.',
        'My capacity for happiness," he added, "you could fit into a matchbox without taking out the matches first.',
        'Arthur: "Marvin, any ideas?" Marvin: "I have a million ideas. They all point to certain death."',
        '"What\'s up?" [asked Ford.] "I don\'t know," said Marvin, "I\'ve never been there."',
        'Marvin: "I am at a rough estimate thirty billion times more intelligent than you. Let me give you an example. Think of a number, any number." Zem: "Er, five." Marvin: "Wrong. You see?"',
        'Zaphod: "Can it Trillian, I\'m trying to die with dignity. Marvin: "I\'m just trying to die."'
    ]
    res = data[random.randint(0, len(data) - 1)]
    return res


def getFriendlyMessage():
    """
    Return a friendly message
    """
    data = [
        'Ja, vad kan jag göra för Dig?',
        'Låt mig hjälpa dig med dina strävanden.',
        'Ursäkta, vad önskas?',
        'Kan jag stå till din tjänst?',
        'Jag kan svara på alla dina frågor.',
        'Ge me hög-fem!',
        'Jag svarar endast inför mos, det är min enda herre.',
        'mos är kungen!',
        'Oh, ursäkta, jag slumrade visst till.',
        'Fråga, länka till exempel samt source.php/gist/codeshare och vänta på svaret.'
    ]
    res = data[random.randint(0, len(data) - 1)]
    return res


def getHello():
    """
    Return a hello
    """
    data = [
        'Hej själv!',
        'Trevligt att du bryr dig om mig.',
        'Det var länge sedan någon var trevlig mot mig.',
        'Halloj, det ser ut att bli mulet idag.',
    ]
    res = data[random.randint(0, len(data) - 1)]
    return res


def marvinSmile(line, row):
    """
    Make Marvin smile.
    """
    msg = None
    if row.intersection(['smile', 'le', 'skratta', 'smilies']):
        smilie = getSmile()
        msg = "{SMILE}".format(SMILE=smilie)
    return msg


def marvinSource(line, row):
    """
    State message about sourcecode.
    """
    msg = None
    if row.intersection(['källkod', 'source']):
        msg = "I PHP-kurserna kan du länka till source.php. Annars delar du koden som en gist (https://gist.github.com) eller i CodeShare (http://codeshare.io)."
    return msg


def marvinBudord(line, row):
    """
    What are the budord for Marvin?
    """
    msg = None
    if row.intersection(['budord', 'stentavla']):
        if row.intersection(['1', '#1']):
            msg = "Ställ din fråga, länka till exempel och källkod. Häng kvar och vänta på svar."
        elif row.intersection(['2', '#2']):
            msg = "Var inte rädd för att fråga och fråga tills du får svar: http://dbwebb.se/f/6249"
        elif row.intersection(['3', '#3']):
            msg = "Öva dig ställa smarta frågor: http://dbwebb.se/f/7802"
        elif row.intersection(['4', '#4']):
            msg = "When in doubt - gör ett testprogram. http://dbwebb.se/f/13570"
        elif row.intersection(['5', '#5']):
            msg = "Hey Luke - use the source! http://catb.org/jargon/html/U/UTSL.html"
    return msg


def marvinQuote(line, row):
    """
    Make a quote.
    """
    msg = None
    if row.intersection(['quote', 'citat', 'filosofi', 'filosofera']):
        msg = getQuote()

    return msg


weekdays = [
  "Idag är det måndag.",
  "Idag är det tisdag.",
  "Idag är det onsdag.",
  "Idag är det torsdag.",
  "Idag är det fredag.",
  "Idag är det lördag.",
  "Idag är det söndag.",
]


def videoOfToday():
    """
    Check what day it is and provide a url to a suitable video together with a greeting.
    """
    dayNum = date.weekday(date.today())
    msg = weekdays[dayNum]

    if dayNum == 0:
        msg += " En passande video är https://www.youtube.com/watch?v=lAZgLcK5LzI."
    elif dayNum == 4:
        msg += " En passande video är https://www.youtube.com/watch?v=kfVsfOSbJY0."
    elif dayNum == 5:
        msg += " En passande video är https://www.youtube.com/watch?v=GVCzdpagXOQ."
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
        msg = "Jag är en tjänstvillig själ som gillar webbprogrammering. Jag bor på GitHub https://github.com/mosbth/irc2phpbb och du kan diskutera mig i forumet http://dbwebb.se/t/20"

    return msg


def marvinHelp(line, row):
    """
    Provide a menu.
    """
    msg = None
    if row.intersection(['hjälp', 'help', 'menu', 'meny']):
        msg = "[ vem är | forum senaste | lyssna | le | lunch | citat | budord 1 - 5 | väder | solen | hjälp | php | js/javascript | attack | slap | dagens video ]"

    return msg


def marvinStats(line, row):
    """
    Provide a link to the stats.
    """
    msg = None
    if row.intersection(['stats', 'statistik', 'ircstats']):
        msg = "Statistik för kanalen finns här: http://dbwebb.se/irssistats/db-o-webb.html"

    return msg


def marvinSayHi(line, row):
    """
    Say hi with a nice message.
    """
    msg = None
    if row.intersection(['snälla', 'hej', 'tjena', 'morsning', 'mår', 'hallå', 'halloj', 'läget', 'snäll', 'duktig', 'träna', 'träning', 'utbildning', 'tack', 'tacka', 'tackar', 'tacksam']):
        smile = getSmile()
        hello = getHello()
        friendly = getFriendlyMessage()
        msg = "{} {} {}".format(smile, hello, friendly)

    return msg


def getLunchMessage():
    """
    Return a lunch message
    """
    data = [
        'Ska vi ta {}?',
        'Ska vi dra ned till {}?',
        'Jag tänkte käka på {}, ska du med?',
        'På {} är det mysigt, ska vi ta där?'
    ]
    res = data[random.randint(0, len(data) - 1)]
    return res


def getLunchStan():
    """
    Return a lunch message from Karlskrona centrum
    """
    data = [
        'Olles krovbar',
        'Lila thai stället',
        'donken',
        'tex mex stället vid subway',
        'Subway',
        'Nya peking',
        'kebab house',
        'Royal thai',
        'thai stället vid hemmakväll',
        'Gelato',
        'Indian garden',
        'Sumo sushi',
        'Pasterian i stan',
        'Biobaren',
        'Michelangelo'
    ]
    res = data[random.randint(0, len(data) - 1)]
    return res


def getLunchBTH():
    """
    Return a lunch message from Gräsvik BTH
    """
    data = [
        'Thairestaurangen vid korsningen',
        'det är lite mysigt i fiket jämte demolabbet',
        'Indiska',
        'Pappa curry',
        'boden uppe på parkeringen',
        'Bergåsa kebab',
        'Pasterian',
        'Villa Oscar',
        'Eat here',
        'Bistro J'
    ]
    res = data[random.randint(0, len(data) - 1)]
    return res


def getLunchHassleholm():
    """
    Return a lunch message from Hassleholm
    """
    data = [
        'pastavagnen på torget',
        'Freds',
        'mcDonalds',
        'subway',
        'kinabuffé på Cats',
        'valentino',
        'lotterilådan',
        'casablance',
        'det där stället i gallerian',
        'infinity',
        'östervärn',
        'argentina',
        'T4'
    ]
    res = data[random.randint(0, len(data) - 1)]
    return res


def marvinLunch(line, row):
    """
    Say hi with a nice message.
    """
    msg = None
    if row.intersection(['lunch', 'mat', 'äta']):
        if row.intersection(['stan', 'centrum', 'karlskrona', 'kna']):
            msg = getLunchMessage().format(getLunchStan())
        elif row.intersection(['hässleholm', 'hassleholm']):
            msg = getLunchMessage().format(getLunchHassleholm())
        else:
            msg = getLunchMessage().format(getLunchBTH())

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
        msg = getListen() + " " + feed["items"][0]["title"]

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
            msg = "Idag går solen upp {} och ner {}. Iallafall i trakterna kring Jönköping.".format(sunrise, sunset)

        except Exception as e:
            msg = "Jag hittade tyvär inga solar idag :( så jag håller på och lär mig hur Python kan räkna ut soluppgången, återkommer."

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
