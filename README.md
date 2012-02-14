Marvin, an IRC bot
==================

The python script, `irc2phpbb.py`, is a implementation of an irc bot keeping track of latest posts in a
phpbb forum. The basic code is from: http://osix.net/modules/article/?id=780 and 
http://oreilly.com/pub/h/1968. From there its further developed and customised to fit the target
forum and target irc-channel.

The rfc for the irc protocol is quite helpful: http://www.irchelp.org/irchelp/rfc/


Its customised for dbwebb.se
----------------------------

The bot is created for use in irc://irc.bsnet.se/#db-o-webb which is an irc channel for 
teaching & learning HTML, CSS, JavaScript, PHP, SQL and Unix. The forum is http://dbwebb.se/forum. 

This means that the code contains some settings to actually work in that environment.


Using feedparser to get RSS-feeds
---------------------------------

The bot uses the `feedparser` python lib to parse RSS feeds, for example when getting the latest post to
the forum. You'll have to download and install the lib yourself.

* http://wiki.python.org/moin/RssLibraries
* http://code.google.com/p/feedparser/


Using BeautifulSoup to scrap web-pages
--------------------------------------

The bot uses the python lib `BeautifulSoup` to scrap information from webpages. Just to show it 
off how its done but it can of course be made into some useful stuff. 
You'll have to download and install the lib yourself.

* http://www.crummy.com/software/BeautifulSoup/


Using PHP to keep track on recent posts
---------------------------------------

The file `aggregate.php` uses `magpierss` (http://magpierss.sourceforge.net/) to aggregate feeds from
several places and while discovering new entries it stores messages in the directory `incoming
where Marvin (the bot) is looking, when finding a file its content will be posted to the 
irc-channel by the bot. You'll have to download and install the lib yourself.

Run `aggregate.php` from crontab with regular intervalls, for example each 5 minute.
  
  */5 * * * * /usr/local/bin/php /home/mos/git/irc2phpbb/aggregate.php

The id of the feed items are stored in a SQLite database to avoid duplicates being posted.


History
-------

Todo.

* aggregate.php, remove duplicate post in same thread. Only show one.


v0.1.0 (2012-02-14) 

* First tag after some live testing for a couple of months. Must start somewhere. 

 .   
..:  Copyright 2011 by Mikael Roos (me@mikaelroos.se)
