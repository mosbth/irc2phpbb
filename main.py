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
import getopt
import json
import os
import sys

import marvin
import marvin_actions
import marvin_general_actions

#
# General stuff about this program
#
PROGRAM = "marvin"
AUTHOR = "Mikael Roos"
EMAIL = "mikael.t.h.roos@gmail.com"
VERSION = "0.3.0"
MSG_USAGE = """{program} - Act as an IRC bot and do useful things.
By {author} ({email}), version {version}.

Usage:
  {program} [options]

Options:
  -h --help       Display this help message.
  -v --version    Print version and exit.
  --config=       Use this file as configfile.
  --server=       Set the IRC server to connect to.
  --port=         Set the port to use, default is 6667.
  --channel=      Set what channel to join.
  --nick=         Set nick to identify by.
  --realname=     Set realname for verbose presentation.
  --ident=        Set password for IDENTIFY for nick.

GitHub: https://github.com/mosbth/irc2phpbb
Issues: https://github.com/mosbth/irc2phpbb/issues
""".format(program=PROGRAM, author=AUTHOR, email=EMAIL, version=VERSION)

MSG_VERSION = "{program} version {version}.".format(program=PROGRAM, version=VERSION)

MSG_USAGE_SHORT = "Use {program} --help to get usage.\n".format(program=PROGRAM)


def printUsage(exitStatus):
    """
    Print usage information about the script and exit.
    """
    print(MSG_USAGE)
    sys.exit(exitStatus)


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
        with open(configFile) as f:
            data = json.load(f)

        options.update(data)
        res = json.dumps(options, sort_keys=True, indent=4, separators=(',', ': '))

        msg = "Read configuration from config file '{file}'. Current configuration is:\n{config}"
        print(msg.format(config=res, file=configFile))

    else:
        print("Config file '{file}' is not readable, skipping.".format(file=configFile))

    return options


def parseOptions():
    """
    Merge default options with incoming options and arguments and return them as a dictionary.
    """

    # Default options to start with
    options = marvin.getConfig()

    # Read from config file if available
    options.update(mergeOptionsWithConfigFile(options, "marvin_config.json"))

    # Switch through all options, commandline options overwrites.
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hv", [
            "help",
            "version",
            "config=",
            "server=",
            "port=",
            "channel=",
            "nick=",
            "realname=",
            "ident="
        ])

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                printUsage(0)

            elif opt in ("-v", "--version"):
                printVersion()

            elif opt in "--config":
                options = mergeOptionsWithConfigFile(options, arg)

            elif opt in "--server":
                options["server"] = arg

            elif opt in "--port":
                options["port"] = arg

            elif opt in "--channel":
                options["channel"] = arg

            elif opt in "--nick":
                options["nick"] = arg

            elif opt in "--realname":
                options["realname"] = arg

            elif opt in "--ident":
                options["ident"] = arg

            else:
                raise Exception("Unhandled option")

        if args:
            raise Exception("Too many arguments, unknown argument.")

    except Exception as err:
        print(err)
        print(MSG_USAGE_SHORT)
        sys.exit(1)

    res = json.dumps(options, sort_keys=True, indent=4, separators=(',', ': '))
    print("Configuration updated after cli options:\n{config}".format(config=res))

    return options


def main():
    """
    Main function to carry out the work.
    """
    options = parseOptions()
    marvin.setConfig(options)
    marvin_actions.setConfig(options)
    marvin_general_actions.setConfig(options)
    actions = marvin_actions.getAllActions()
    general_actions = marvin_general_actions.getAllGeneralActions()
    marvin.registerActions(actions)
    marvin.registerGeneralActions(general_actions)
    marvin.connectToServer()
    marvin.mainLoop()

    sys.exit(0)


if __name__ == "__main__":
    main()
