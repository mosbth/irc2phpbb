#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module for the IRC bot.

Connecting, sending and receiving messages and doing custom actions.

Keeping a log and reading incoming material.
"""
import logging
import os
import shutil
import socket

import chardet

from bot import Bot

LOG = logging.getLogger("bot")

class IrcBot(Bot):
    """Bot implementing the IRC protocol"""
    def __init__(self):
        super().__init__()
        self.CONFIG = {
            "server": None,
            "port": 6667,
            "channel": None,
            "nick": "marvin",
            "realname": "Marvin The All Mighty dbwebb-bot",
            "ident": None,
            "dirIncoming": "incoming",
            "dirDone": "done",
            "lastfm": None,
        }

        # Socket for IRC server
        self.SOCKET = None

    def connectToServer(self):
        """Connect to the IRC Server"""

        # Create the socket  & Connect to the server
        server = self.CONFIG["server"]
        port = self.CONFIG["port"]

        if server and port:
            self.SOCKET = socket.socket()
            LOG.info("Connecting: %s:%d", server, port)
            self.SOCKET.connect((server, port))
        else:
            LOG.error("Failed to connect, missing server or port in configuration.")
            return

        # Send the nick to server
        nick = self.CONFIG["nick"]
        if nick:
            msg = f'NICK {nick}\r\n'
            self.sendMsg(msg)
        else:
            LOG.info("Ignore sending nick, missing nick in configuration.")

        # Present yourself
        realname = self.CONFIG["realname"]
        self.sendMsg(f'USER  {nick} 0 * :{realname}\r\n')

        # This is my nick, i promise!
        ident = self.CONFIG["ident"]
        if ident:
            self.sendMsg(f'PRIVMSG nick IDENTIFY {ident}\r\n')
        else:
            LOG.info("Ignore identifying with password, ident is not set.")

        # Join a channel
        channel = self.CONFIG["channel"]
        if channel:
            self.sendMsg(f'JOIN {channel}\r\n')
        else:
            LOG.info("Ignore joining channel, missing channel name in configuration.")

    def sendPrivMsg(self, message, channel):
        """Send and log a PRIV message"""
        if channel == self.CONFIG["channel"]:
            self.MSG_LOG.debug("%s <%s>  %s", channel, self.CONFIG["nick"], message)

        msg = f"PRIVMSG {channel} :{message}\r\n"
        self.sendMsg(msg)

    def sendMsg(self, msg):
        """Send and occasionally print the message sent"""
        LOG.debug("SEND: %s", msg.rstrip("\r\n"))
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
        res = None
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
        lines = None
        try:
            buf = self.SOCKET.recv(2048)
            lines = self.decode_irc(buf)
            lines = lines.split("\n")
            buf = lines.pop()
        except Exception as err:
            LOG.error("Error reading incoming message %s", err)

        return lines

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
                LOG.warning("Failed to move %s to %s. Deleting.", filename, self.CONFIG["dirDone"])
                os.remove(filename)

    def mainLoop(self):
        """For ever, listen and answer to incoming chats"""
        while 1:
            # Check in any in the incoming directory
            self.readincoming()

            for line in self.receive():
                LOG.debug(line)
                words = line.strip().split()

                if not words:
                    continue

                self.checkIrcActions(words)
                self.checkMarvinActions(words)

    def begin(self):
        """Start the bot"""
        self.connectToServer()
        self.mainLoop()

    def checkIrcActions(self, words):
        """
        Check if Marvin should take action on any messages defined in the
        IRC protocol.
        """
        if words[0] == "PING":
            self.sendMsg(f"PONG {words[1]}\r\n")

        if words[1] == 'INVITE':
            self.sendMsg(f'JOIN {words[3]}\r\n')

    def checkMarvinActions(self, words):
        """Check if Marvin should perform any actions"""
        if words[1] == 'PRIVMSG' and words[2] == self.CONFIG["channel"]:
            self.MSG_LOG.debug("%s <%s>  %s",
                               words[2],
                               words[0].split(":")[1].split("!")[0],
                               " ".join(words[3:]))

        if words[1] == 'PRIVMSG':
            raw = ' '.join(words[3:])
            row = self.tokenize(raw)

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
