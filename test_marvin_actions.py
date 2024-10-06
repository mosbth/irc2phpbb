#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests for all Marvin actions
"""

import json

from datetime import date
from unittest import mock, TestCase

import requests

from bot import Bot
import marvin_actions
import marvin_general_actions

class ActionTest(TestCase):
    """Test Marvin actions"""
    strings = {}

    @classmethod
    def setUpClass(cls):
        with open("marvin_strings.json", encoding="utf-8") as f:
            cls.strings = json.load(f)


    def executeAction(self, action, message):
        """Execute an action for a message and return the response"""
        return action(Bot.tokenize(message))


    def assertActionOutput(self, action, message, expectedOutput):
        """Call an action on message and assert expected output"""
        actualOutput = self.executeAction(action, message)

        self.assertEqual(actualOutput, expectedOutput)


    def assertActionSilent(self, action, message):
        """Call an action with provided message and assert no output"""
        self.assertActionOutput(action, message, None)


    def assertStringsOutput(self, action, message, expectedoutputKey, subkey=None):
        """Call an action with provided message and assert the output is equal to DB"""
        expectedOutput = self.strings.get(expectedoutputKey)
        if subkey is not None:
            if isinstance(expectedOutput, list):
                expectedOutput = expectedOutput[subkey]
            else:
                expectedOutput = expectedOutput.get(subkey)
        self.assertActionOutput(action, message, expectedOutput)


    def assertBBQResponse(self, todaysDate, bbqDate, expectedMessageKey):
        """Assert that the proper bbq message is returned, given a date"""
        url = self.strings.get("barbecue").get("url")
        message = self.strings.get("barbecue").get(expectedMessageKey)
        if isinstance(message, list):
            message = message[1]
        if expectedMessageKey in ["base", "week", "eternity"]:
            message = message % bbqDate

        with mock.patch("marvin_actions.datetime") as d:
            d.date.today.return_value = todaysDate
            with mock.patch("marvin_actions.random") as r:
                r.randint.return_value = 1
                expected = f"{url}. {message}"
                self.assertActionOutput(marvin_actions.marvinTimeToBBQ, "dags att grilla", expected)


    def assertNameDayOutput(self, exampleFile, expectedOutput):
        """Assert that the proper nameday message is returned, given an inputfile"""
        with open(f"namedayFiles/{exampleFile}.json", "r", encoding="UTF-8") as f:
            response = requests.models.Response()
            response._content = str.encode(json.dumps(json.load(f)))
            with mock.patch("marvin_actions.requests") as r:
                r.get.return_value = response
                self.assertActionOutput(marvin_actions.marvinNameday, "nameday", expectedOutput)

    def assertJokeOutput(self, exampleFile, expectedOutput):
        """Assert that a joke is returned, given an input file"""
        with open(f"jokeFiles/{exampleFile}.json", "r", encoding="UTF-8") as f:
            response = requests.models.Response()
            response._content = str.encode(json.dumps(json.load(f)))
            with mock.patch("marvin_actions.requests") as r:
                r.get.return_value = response
                self.assertActionOutput(marvin_actions.marvinJoke, "joke", expectedOutput)

    def testSmile(self):
        """Test that marvin can smile"""
        with mock.patch("marvin_actions.random") as r:
            r.randint.return_value = 1
            self.assertStringsOutput(marvin_actions.marvinSmile, "le lite?", "smile", 1)
        self.assertActionSilent(marvin_actions.marvinSmile, "sur idag?")

    def testWhois(self):
        """Test that marvin responds to whois"""
        self.assertStringsOutput(marvin_actions.marvinWhoIs, "vem är marvin?", "whois")
        self.assertActionSilent(marvin_actions.marvinWhoIs, "vemär")

    def testGoogle(self):
        """Test that marvin can help google stuff"""
        with mock.patch("marvin_actions.random") as r:
            r.randint.return_value = 1
            self.assertActionOutput(
                marvin_actions.marvinGoogle,
                "kan du googla mos",
                "LMGTFY https://www.google.se/search?q=mos")
            self.assertActionOutput(
                marvin_actions.marvinGoogle,
                "kan du googla google mos",
                "LMGTFY https://www.google.se/search?q=google+mos")
        self.assertActionSilent(marvin_actions.marvinGoogle, "du kan googla")
        self.assertActionSilent(marvin_actions.marvinGoogle, "gogool")

    def testExplainShell(self):
        """Test that marvin can explain shell commands"""
        url = "http://explainshell.com/explain?cmd=pwd"
        self.assertActionOutput(marvin_actions.marvinExplainShell, "explain pwd", url)
        self.assertActionOutput(marvin_actions.marvinExplainShell, "can you explain pwd", url)
        self.assertActionOutput(
            marvin_actions.marvinExplainShell,
            "förklara pwd|grep -o $user",
            f"{url}%7Cgrep+-o+%24user")

        self.assertActionSilent(marvin_actions.marvinExplainShell, "explains")

    def testSource(self):
        """Test that marvin responds to questions about source code"""
        self.assertStringsOutput(marvin_actions.marvinSource, "source", "source")
        self.assertStringsOutput(marvin_actions.marvinSource, "källkod", "source")
        self.assertActionSilent(marvin_actions.marvinSource, "opensource")

    def testBudord(self):
        """Test that marvin knows all the commandments"""
        for n in range(1, 5):
            self.assertStringsOutput(marvin_actions.marvinBudord, f"budord #{n}", "budord", f"#{n}")

        self.assertStringsOutput(marvin_actions.marvinBudord,"visa stentavla 1", "budord", "#1")
        self.assertActionSilent(marvin_actions.marvinBudord, "var är stentavlan?")

    def testQuote(self):
        """Test that marvin can quote The Hitchhikers Guide to the Galaxy"""
        with mock.patch("marvin_actions.random") as r:
            r.randint.return_value = 1
            self.assertStringsOutput(marvin_actions.marvinQuote, "ge os ett citat", "hitchhiker", 1)
            self.assertStringsOutput(marvin_actions.marvinQuote, "filosofi", "hitchhiker", 1)
            self.assertStringsOutput(marvin_actions.marvinQuote, "filosofera", "hitchhiker", 1)
            self.assertActionSilent(marvin_actions.marvinQuote, "noquote")

            for i,_ in enumerate(self.strings.get("hitchhiker")):
                r.randint.return_value = i
                self.assertStringsOutput(marvin_actions.marvinQuote, "quote", "hitchhiker", i)

    def testVideoOfToday(self):
        """Test that marvin can link to a different video each day of the week"""
        with mock.patch("marvin_actions.datetime") as dt:
            for d in range(1, 8):
                dt.date.weekday.return_value = d - 1
                day =  self.strings.get("weekdays").get(str(d))
                video = self.strings.get("video-of-today").get(str(d))
                response = f"{day} En passande video är {video}"
                self.assertActionOutput(marvin_actions.marvinVideoOfToday, "dagens video", response)
        self.assertActionSilent(marvin_actions.marvinVideoOfToday, "videoidag")

    def testHelp(self):
        """Test that marvin can provide a help menu"""
        self.assertStringsOutput(marvin_actions.marvinHelp, "help", "menu")
        self.assertActionSilent(marvin_actions.marvinHelp, "halp")

    def testStats(self):
        """Test that marvin can provide a link to the IRC stats page"""
        self.assertStringsOutput(marvin_actions.marvinStats, "stats", "ircstats")
        self.assertActionSilent(marvin_actions.marvinStats, "statistics")

    def testIRCLog(self):
        """Test that marvin can provide a link to the IRC log"""
        self.assertStringsOutput(marvin_actions.marvinIrcLog, "irc", "irclog")
        self.assertActionSilent(marvin_actions.marvinIrcLog, "ircstats")

    def testSayHi(self):
        """Test that marvin responds to greetings"""
        with mock.patch("marvin_actions.random") as r:
            for skey, s in enumerate(self.strings.get("smile")):
                for hkey, h in enumerate(self.strings.get("hello")):
                    for fkey, f in enumerate(self.strings.get("friendly")):
                        r.randint.side_effect = [skey, hkey, fkey]
                        self.assertActionOutput(marvin_actions.marvinSayHi, "hej", f"{s} {h} {f}")
        self.assertActionSilent(marvin_actions.marvinSayHi, "korsning")

    def testLunchLocations(self):
        """Test that marvin can provide lunch suggestions for certain places"""
        locations = ["karlskrona", "goteborg", "angelholm", "hassleholm", "malmo"]
        with mock.patch("marvin_actions.random") as r:
            for location in locations:
                for index, place in enumerate(self.strings.get(f"lunch-{location}")):
                    r.randint.side_effect = [0, index]
                    self.assertActionOutput(
                        marvin_actions.marvinLunch, f"mat {location}", f"Ska vi ta {place}?")
            r.randint.side_effect = [1, 2]
            self.assertActionOutput(
                marvin_actions.marvinLunch, "dags att luncha", "Jag är lite sugen på Indiska?")
        self.assertActionSilent(marvin_actions.marvinLunch, "matdags")

    def testStrip(self):
        """Test that marvin can recommend comics"""
        messageFormat = self.strings.get("commitstrip").get("message")
        expected = messageFormat.format(url=self.strings.get("commitstrip").get("url"))
        self.assertActionOutput(marvin_actions.marvinStrip, "lite strip kanske?", expected)
        self.assertActionSilent(marvin_actions.marvinStrip, "nostrip")

    def testRandomStrip(self):
        """Test that marvin can recommend random comics"""
        messageFormat = self.strings.get("commitstrip").get("message")
        expected = messageFormat.format(url=self.strings.get("commitstrip").get("urlPage") + "123")
        with mock.patch("marvin_actions.random") as r:
            r.randint.return_value = 123
            self.assertActionOutput(marvin_actions.marvinStrip, "random strip kanske?", expected)

    def testTimeToBBQ(self):
        """Test that marvin knows when the next BBQ is"""
        self.assertBBQResponse(date(2024, 5, 17), date(2024, 5, 17), "today")
        self.assertBBQResponse(date(2024, 5, 16), date(2024, 5, 17), "tomorrow")
        self.assertBBQResponse(date(2024, 5, 10), date(2024, 5, 17), "week")
        self.assertBBQResponse(date(2024, 5, 1), date(2024, 5, 17), "base")
        self.assertBBQResponse(date(2023, 10, 17), date(2024, 5, 17), "eternity")

        self.assertBBQResponse(date(2024, 9, 20), date(2024, 9, 20), "today")
        self.assertBBQResponse(date(2024, 9, 19), date(2024, 9, 20), "tomorrow")
        self.assertBBQResponse(date(2024, 9, 13), date(2024, 9, 20), "week")
        self.assertBBQResponse(date(2024, 9, 4), date(2024, 9, 20), "base")

    def testNameDayReaction(self):
        """Test that marvin only responds to nameday when asked"""
        self.assertActionSilent(marvin_actions.marvinNameday, "anything")

    def testNameDayRequest(self):
        """Test that marvin sends a proper request for nameday info"""
        with mock.patch("marvin_actions.requests") as r:
            with mock.patch("marvin_actions.datetime") as d:
                d.datetime.now.return_value = date(2024, 1, 2)
                self.executeAction(marvin_actions.marvinNameday, "namnsdag")
                self.assertEqual(r.get.call_args.args[0], "http://api.dryg.net/dagar/v2.1/2024/1/2")

    def testNameDayResponse(self):
        """Test that marvin properly parses nameday responses"""
        self.assertNameDayOutput("single", "Idag har Svea namnsdag")
        self.assertNameDayOutput("double", "Idag har Alfred,Alfrida namnsdag")
        self.assertNameDayOutput("nobody", "Ingen har namnsdag idag")

    def testJokeRequest(self):
        """Test that marvin sends a proper request for a joke"""
        with mock.patch("marvin_actions.requests") as r:
            self.executeAction(marvin_actions.marvinJoke, "joke")
            self.assertEqual(
                r.get.call_args.args[0],
                "https://api.chucknorris.io/jokes/random?category=dev")

    def testJoke(self):
        """Test that marvin sends a joke when requested"""
        self.assertJokeOutput("joke", "There is no Esc key on Chuck Norris' keyboard, because no one escapes Chuck Norris.")

    def testUptime(self):
        """Test that marvin can provide the link to the uptime tournament"""
        self.assertStringsOutput(marvin_actions.marvinUptime, "visa lite uptime", "uptime", "info")
        self.assertActionSilent(marvin_actions.marvinUptime, "uptimetävling")

    def testStream(self):
        """Test that marvin can provide the link to the stream"""
        self.assertStringsOutput(marvin_actions.marvinStream, "ska mos streama?", "stream", "info")
        self.assertActionSilent(marvin_actions.marvinStream, "är mos en streamer?")

    def testPrinciple(self):
        """Test that marvin can recite some software principles"""
        principles = self.strings.get("principle")
        for key, value in principles.items():
            self.assertActionOutput(marvin_actions.marvinPrinciple, f"princip {key}", value)
        with mock.patch("marvin_actions.random") as r:
            r.choice.return_value = "dry"
            self.assertStringsOutput(marvin_actions.marvinPrinciple, "princip", "principle", "dry")
        self.assertActionSilent(marvin_actions.marvinPrinciple, "principlös")

    def testCommitRequest(self):
        """Test that marvin sends proper requests when generating commit messages"""
        with mock.patch("marvin_actions.requests") as r:
            self.executeAction(marvin_actions.marvinCommit, "vad skriver man efter commit -m?")
            self.assertEqual(r.get.call_args.args[0], "http://whatthecommit.com/index.txt")

    def testCommitResponse(self):
        """Test that marvin properly handles responses when generating commit messages"""
        message = "Secret sauce #9"
        response = requests.models.Response()
        response._content = str.encode(message)
        with mock.patch("marvin_actions.requests") as r:
            r.get.return_value = response
            expected = f"Använd detta meddelandet: '{message}'"
            self.assertActionOutput(marvin_actions.marvinCommit, "commit", expected)

    def testMorning(self):
        """Test that marvin wishes good morning, at most once per day"""
        marvin_general_actions.lastDateGreeted = None
        with mock.patch("marvin_general_actions.datetime") as d:
            d.date.today.return_value = date(2024, 5, 17)
            with mock.patch("marvin_general_actions.random") as r:
                r.choice.return_value = "Morgon"
                self.assertActionOutput(marvin_general_actions.marvinMorning, "morrn", "Morgon")
                # Should only greet once per day
                self.assertActionSilent(marvin_general_actions.marvinMorning, "morgon")
                # Should greet again tomorrow
                d.date.today.return_value = date(2024, 5, 18)
                self.assertActionOutput(marvin_general_actions.marvinMorning, "godmorgon", "Morgon")
