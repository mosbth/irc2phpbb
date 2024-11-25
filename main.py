#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
An IRC bot that answers random questions, keeps a log from the IRC-chat,
easy to integrate in a webpage and montores a phpBB forum for latest topics
by loggin in to the forum and checking the RSS-feed.

You need to install additional modules.

# Install needed modules in local directory
pip3 install --target modules/ feedparser beautifulsoup4 chardet

Modules in modules/ will be loaded automatically. If you want to use a
different directory you can start the program like this instead:

PYTHONPATH=modules python3 main.py

# To get help
PYTHONPATH=modules python3 main.py --help

# Example of using options
--server=irc.bsnet.se --channel=#db-o-webb
--server=irc.bsnet.se --port=6667 --channel=#db-o-webb
--nick=marvin --ident=secret

# Configuration
Check out the file 'marvin_config_default.json' on how to configure, instead
of using cli-options. The default configfile is 'marvin_config.json' but you
can change that using cli-options.

# Make own actions
Check the file 'marvin_strings.json' for the file where most of the strings
are defined and check out 'marvin_actions.py' to see how to write your own
actions. Its just a small function.

# Read from incoming
Marvin reads messages from the incoming/ directory, if it exists, and writes
it out the the irc channel.
"""

import argparse
import json
import logging
import logging.config
import os
import sys

from discord_bot import DiscordBot
from irc_bot import IrcBot

import marvin_actions
import marvin_general_actions

#
# General stuff about this program
#
PROGRAM = "marvin"
AUTHOR = "Mikael Roos"
EMAIL = "mikael.t.h.roos@gmail.com"
VERSION = "0.3.0"
MSG_VERSION = f"{PROGRAM} version {VERSION}."

LOG = logging.getLogger("main")


def printVersion():
    """
    Print version information and exit.
    """
    print(MSG_VERSION)
    sys.exit(0)


def mergeOptionsWithConfigFile(options, configFile):
    """
    Read information from config file.
    """
    if os.path.isfile(configFile):
        with open(configFile, encoding="UTF-8") as f:
            data = json.load(f)

        options.update(data)
        res = json.dumps(options, sort_keys=True, indent=4, separators=(',', ': '))
        LOG.info("Read configuration from config file '%s'.", configFile)
        LOG.info("Current configuration is: %s", res)
    else:
        LOG.info("Config file '{%s}' is not readable, skipping.", configFile)

    return options


def parseOptions(options):
    """
    Merge default options with incoming options and arguments and return them as a dictionary.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("protocol", choices=["irc", "discord"], nargs="?", default="irc")
    parser.add_argument("-v", "--version", action="store_true")
    parser.add_argument("--config")

    for key, value in options.items():
        parser.add_argument(f"--{key}", type=type(value))

    args = vars(parser.parse_args())
    if args["version"]:
        printVersion()
    if args["config"]:
        mergeOptionsWithConfigFile(options, args["config"])

    for parameter in options:
        if args[parameter]:
            options[parameter] = args[parameter]

    res = json.dumps(options, sort_keys=True, indent=4, separators=(',', ': '))
    LOG.info("Configuration updated after cli options: %s", res)

    return options


def determineProtocol():
    """Parse the argument to determine what protocol to use"""
    parser = argparse.ArgumentParser()
    parser.add_argument("protocol", choices=["irc", "discord"], nargs="?", default="irc")
    arg, _ = parser.parse_known_args()
    return arg.protocol


def createBot(protocol):
    """Return an instance of a bot with the requested implementation"""
    if protocol == "irc":
        return IrcBot()
    if protocol == "discord":
        return DiscordBot()
    raise ValueError(f"Unsupported protocol: {protocol}")


def setupLogging():
    """Set up the logging config"""
    with open("logging.json", encoding="UTF-8") as f:
        config = json.load(f)
    logging.config.dictConfig(config)

def main():
    """
    Main function to carry out the work.
    """
    setupLogging()
    protocol = determineProtocol()
    bot = createBot(protocol)
    options = bot.getConfig()
    options.update(mergeOptionsWithConfigFile(options, "marvin_config.json"))
    config = parseOptions(options)
    bot.setConfig(config)
    actions = marvin_actions.getAllActions()
    general_actions = marvin_general_actions.getAllGeneralActions()
    bot.registerActions(actions)
    bot.registerGeneralActions(general_actions)
    bot.begin()

    sys.exit(0)


if __name__ == "__main__":
    main()
