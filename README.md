Marvin, an IRC/discord bot
==================

[![Build Status GitHub Actions](https://github.com/mosbth/irc2phpbb/actions/workflows/main.yml/badge.svg)](https://github.com/mosbth/irc2phpbb/actions)
[![Build Status Scrutinizer](https://scrutinizer-ci.com/g/mosbth/irc2phpbb/badges/build.png?b=master)](https://scrutinizer-ci.com/g/mosbth/irc2phpbb/build-status/master)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/mosbth/irc2phpbb/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/mosbth/irc2phpbb/?branch=master)
[![Code Coverage](https://scrutinizer-ci.com/g/mosbth/irc2phpbb/badges/coverage.png?b=master)](https://scrutinizer-ci.com/g/mosbth/irc2phpbb/?branch=master)
=======

Marvin was originally an IRC bot (now also supporting discord) that responds to basic questions and provides guidance in the life of anyone involved in any [dbwebb](https://www.dbwebb.se) courses. 


Contribute
--------------------------

Before you actually start contributing, create an issue and discuss what you want to do. This is just to avoid that your PR will be denied for some random reason. 


This project uses [`uv`](https://github.com/astral-sh/uv) to manage dependencies and tools. Refer their [documentation](https://docs.astral.sh/uv/getting-started/) for instructions how to install it and getting started.


Running tests and code coverage
--------------------------

Run the unittests.

```bash
uv run pytest
```

Run code coverage and report results in terminal.

```bash
uv run pytest --cov=irc2phpbb
```

Run pylint on both production code and the tests.
```bash
uv run pylint irc2phpbb
uv run pylint tests
```

Run code coverage and create an html report. An html report of the code coverage is generated in `htmlcov/index.html`. [Other report formats](https://pytest-cov.readthedocs.io/en/latest/reporting.html) are also supported. If you generate other formats, take care not to commit them to the repository.
```bash
uv run pytest --cov=irc2phpbb --cov-report=html
```

Execute marvin in docker
--------------------------
The easiest way to run marvin in a *real* setting is to run it in IRC mode, as that doesn't require any registration with discord services.


Build the python package and the docker image, then start marvin as a container in the background.
```bash
uv build
docker compose build
docker compose up -d marvin
```

Now you can connect to `localhost` with any IRC client of your choice, or you can follow the instructions below to run [irssi](https://irssi.org/) in a [container](https://hub.docker.com/_/irssi).

```bash
docker compose run --rm irssi
```
You should be automatically connected to the server and join the `#marvin` channel.


When you are done, you can shut down all the containers.
```bash
docker compose down
```

API documentation 
--------------------------

The code and API documentation is generated using [pdoc](https://pdoc.dev/).

```bash
uv run pdoc --output-dir=docs/pdoc irc2phpbb
```
The docs are saved at `docs/pdoc` and can be [viewed online](https://mosbth.github.io/irc2phpbb/pdoc/).



History
--------------------------
The python script, `irc2phpbb.py`, is a implementation of an irc bot. The bot can answer 
simple questions and some more advanced features such as presenting the weather by 
scraping an external website and keeping track of forum posts and posting new posts to 
the channel. The bot is reading incoming entries from a directory and external scripts may 
put information there that should be displayed in the irc-channel.

The PHP-script `aggregate.php` is used to log in to the forum to get credentials to view 
the latest posts through rss. A SQLite database is used to keep track on which posts 
have been displayed in the irc-channel.

The basic code is from: http://osix.net/modules/article/?id=780 and 
http://oreilly.com/pub/h/1968. From there its further developed and customized to fit the target
forum and target irc-channel.

The rfc for the irc protocol is quite helpful: http://www.irchelp.org/irchelp/rfc/

/Mikael Roos (mos@dbwebb.se)


Customized for dbwebb.se
----------------------------

The bot is created for use in irc://irc.bsnet.se/#db-o-webb which is an irc channel for 
teaching & learning HTML, CSS, JavaScript, PHP, SQL and Unix. The forum is http://dbwebb.se/forum. 

This means that the code contains some settings to work in that environment and can therefore
not just be cloned and installed. Modifications are needed. The script may anyhow be useful 
as a study object for those in need of similar functionality.


Using feedparser to get RSS-feeds
---------------------------------

The bot uses the `feedparser` python lib to parse RSS feeds, for example when getting the latest post to
the forum. You'll have to download and install the lib yourself.

* http://wiki.python.org/moin/RssLibraries
* http://code.google.com/p/feedparser/


Using BeautifulSoup to scrape web-pages
--------------------------------------

The bot uses the python lib `BeautifulSoup` to scrape information from webpages. Just to show it 
off how it's done but it can of course be made into some useful stuff. 
You'll have to download and install the lib yourself.

* http://www.crummy.com/software/BeautifulSoup/


Using PHP to keep track on recent posts
---------------------------------------

The file `aggregate.php` uses `magpierss` (http://magpierss.sourceforge.net/) to aggregate feeds from
several places and while discovering new entries it stores messages in the directory `incoming`
where Marvin (the bot) is looking, when finding a file its content will be posted to the 
irc-channel by the bot. You'll have to download and unpack the library in the 'magpierss' folder.
You also need to create the folder 'incoming' and create the database file that will be used. The 
database file should be named db.sqlite and reside in the same folder as aggregate.php. The table 
needed in the database looks like this:

CREATE TABLE aggregate (id INTEGER PRIMARY KEY AUTOINCREMENT, feed text, key text UNIQUE);

Run `aggregate.php` from crontab with regular intervals, for example each 5 minute.

```
*/5 * * * * /usr/local/bin/php /home/mos/git/irc2phpbb/aggregate.php
```
The id of the feed items are stored in a SQLite database to avoid duplicates being posted.



 .   
..:  Copyright 2011-2017 by Mikael Roos (mos@dbwebb.se)
