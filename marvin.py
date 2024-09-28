#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module for the IRC bot.

Connecting, sending and receiving messages and doing custom actions.

Keeping a log and reading incoming material.
"""
from collections import deque
from datetime import datetime
import json
import os
import re
import shutil
import socket

import chardet


class IrcBot():
    """IRC implementation of Marvin"""
    def __init__(self):
        self.CONFIG = {
            "server": None,
            "port": 6667,
            "channel": None,
            "nick": "marvin",
            "realname": "Marvin The All Mighty dbwebb-bot",
            "ident": None,
            "irclogfile": "irclog.txt",
            "irclogmax": 20,
            "dirIncoming": "incoming",
            "dirDone": "done",
            "lastfm": None,
        }

        # Socket for IRC server
        self.SOCKET = None

        # All actions to check for incoming messages
        self.ACTIONS = []
        self.GENERAL_ACTIONS = []

        # Keep a log of the latest messages
        self.IRCLOG = None

    def getConfig(self):
        """Return the current configuration"""
        return self.CONFIG

    def setConfig(self, config):
        """Set the current configuration"""
        self.CONFIG = config

    def registerActions(self, actions):
        """Register actions to use"""
        print("Adding actions:")
        for action in actions:
            print(" - " + action.__name__)
        self.ACTIONS.extend(actions)

    def registerGeneralActions(self, actions):
        """Register general actions to use"""
        print("Adding general actions:")
        for action in actions:
            print(" - " + action.__name__)
        self.GENERAL_ACTIONS.extend(actions)

    def connectToServer(self):
        """Connect to the IRC Server"""

        # Create the socket  & Connect to the server
        server = self.CONFIG["server"]
        port = self.CONFIG["port"]

        if server and port:
            self.SOCKET = socket.socket()
            print("Connecting: {SERVER}:{PORT}".format(SERVER=server, PORT=port))
            self.SOCKET.connect((server, port))
        else:
            print("Failed to connect, missing server or port in configuration.")
            return

        # Send the nick to server
        nick = self.CONFIG["nick"]
        if nick:
            msg = 'NICK {NICK}\r\n'.format(NICK=nick)
            self.sendMsg(msg)
        else:
            print("Ignore sending nick, missing nick in configuration.")

        # Present yourself
        realname = self.CONFIG["realname"]
        self.sendMsg('USER  {NICK} 0 * :{REALNAME}\r\n'.format(NICK=nick, REALNAME=realname))

        # This is my nick, i promise!
        ident = self.CONFIG["ident"]
        if ident:
            self.sendMsg('PRIVMSG nick IDENTIFY {IDENT}\r\n'.format(IDENT=ident))
        else:
            print("Ignore identifying with password, ident is not set.")

        # Join a channel
        channel = self.CONFIG["channel"]
        if channel:
            self.sendMsg('JOIN {CHANNEL}\r\n'.format(CHANNEL=channel))
        else:
            print("Ignore joining channel, missing channel name in configuration.")

    def sendPrivMsg(self, message, channel):
        """Send and log a PRIV message"""
        if channel == self.CONFIG["channel"]:
            self.ircLogAppend(user=self.CONFIG["nick"].ljust(8), message=message)

        msg = "PRIVMSG {CHANNEL} :{MSG}\r\n".format(CHANNEL=channel, MSG=message)
        self.sendMsg(msg)

    def sendMsg(self, msg):
        """Send and occasionally print the message sent"""
        print("SEND: " + msg.rstrip('\r\n'))
        self.SOCKET.send(msg.encode())

    def decode_irc(self, raw, preferred_encs=None):
        """
        Do character detection.
        You can send preferred encodings as a list through preferred_encs.
        http://stackoverflow.com/questions/938870/python-irc-bot-and-encoding-issue
        """
        if preferred_encs is None:
            preferred_encs = ["UTF-8", "CP1252", "ISO-8859-1"]

        changed = False
        enc = None
        for enc in preferred_encs:
            try:
                res = raw.decode(enc)
                changed = True
                break
            except Exception:
                pass

        if not changed:
            try:
                enc = chardet.detect(raw)['encoding']
                res = raw.decode(enc)
            except Exception:
                res = raw.decode(enc, 'ignore')

        return res

    def receive(self):
        """Read incoming message and guess encoding"""
        try:
            buf = self.SOCKET.recv(2048)
            lines = self.decode_irc(buf)
            lines = lines.split("\n")
            buf = lines.pop()
        except Exception as err:
            print("Error reading incoming message. " + err)

        return lines

    def ircLogAppend(self, line=None, user=None, message=None):
        """Read incoming message and guess encoding"""
        if not user:
            user = re.search(r"(?<=:)\w+", line[0]).group(0)

        if not message:
            message = ' '.join(line[3:]).lstrip(':')

        self.IRCLOG.append({
            'time': datetime.now().strftime("%H:%M").rjust(5),
            'user': user,
            'msg': message
        })

    def ircLogWriteToFile(self):
        """Write IRClog to file"""
        with open(self.CONFIG["irclogfile"], 'w', encoding="UTF-8") as f:
            json.dump(list(self.IRCLOG), f, indent=2)

    def readincoming(self):
        """
        Read all files in the directory incoming, send them as a message if
        they exists and then move the file to directory done.
        """
        if not os.path.isdir(self.CONFIG["dirIncoming"]):
            return

        listing = os.listdir(self.CONFIG["dirIncoming"])

        for infile in listing:
            filename = os.path.join(self.CONFIG["dirIncoming"], infile)

            with open(filename, "r", encoding="UTF-8") as f:
                for msg in f:
                    self.sendPrivMsg(msg, self.CONFIG["channel"])

            try:
                shutil.move(filename, self.CONFIG["dirDone"])
            except Exception:
                os.remove(filename)

    def mainLoop(self):
        """For ever, listen and answer to incoming chats"""
        self.IRCLOG = deque([], self.CONFIG["irclogmax"])

        while 1:
            # Write irclog
            self.ircLogWriteToFile()

            # Check in any in the incoming directory
            self.readincoming()

            for line in self.receive():
                print(line)
                words = line.strip().split()

                if not words:
                    continue

                self.checkIrcActions(words)
                self.checkMarvinActions(words)

    def checkIrcActions(self, words):
        """
        Check if Marvin should take action on any messages defined in the
        IRC protocol.
        """
        if words[0] == "PING":
            self.sendMsg("PONG {ARG}\r\n".format(ARG=words[1]))

        if words[1] == 'INVITE':
            self.sendMsg('JOIN {CHANNEL}\r\n'.format(CHANNEL=words[3]))


    def checkMarvinActions(self, words):
        """Check if Marvin should perform any actions"""
        if words[1] == 'PRIVMSG' and words[2] == self.CONFIG["channel"]:
            self.ircLogAppend(words)

        if words[1] == 'PRIVMSG':
            raw = ' '.join(words[3:])
            row = re.sub('[,.?:]', ' ', raw).strip().lower().split()

            if self.CONFIG["nick"] in row:
                for action in self.ACTIONS:
                    msg = action(row)
                    if msg:
                        self.sendPrivMsg(msg, words[2])
                        break
            else:
                for action in self.GENERAL_ACTIONS:
                    msg = action(row)
                    if msg:
                        self.sendPrivMsg(msg, words[2])
                        break
