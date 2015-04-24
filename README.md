Marvin, an IRC bot
==================

The python script, `irc2phpbb.py`, is a implementation of an irc bot. The bot can answer 
simple questions and some more advanced features such as presenting the weather by 
scraping an external website and keeping track of forum posts and posting new posts to 
the channel. The bot is reading incoming entries from a directory and external scripts may 
put information there that should be displayed in the irc-channel.

The PHP-script `aggregate.php` is used to log in to the forum to get credentials to view 
the latest posts through rss. A SQLite database is used to keep track on which posts 
have been displayed in the irc-channel.

The basic code is from: http://osix.net/modules/article/?id=780 and 
http://oreilly.com/pub/h/1968. From there its further developed and customised to fit the target
forum and target irc-channel.

The rfc for the irc protocol is quite helpful: http://www.irchelp.org/irchelp/rfc/

/Mikael Roos (mos@dbwebb.se)


Customised for dbwebb.se
----------------------------

The bot is created for use in irc://irc.bsnet.se/#db-o-webb which is an irc channel for 
teaching & learning HTML, CSS, JavaScript, PHP, SQL and Unix. The forum is http://dbwebb.se/forum. 

This means that the code contains some settings to work in that environment and can therefore
not just be cloned and installed. Modifications are needen. The script may anyhow be useful 
as a studyobject for those in need of simulare functionality.


Using feedparser to get RSS-feeds
---------------------------------

The bot uses the `feedparser` python lib to parse RSS feeds, for example when getting the latest post to
the forum. You'll have to download and install the lib yourself.

* http://wiki.python.org/moin/RssLibraries
* http://code.google.com/p/feedparser/


Using BeautifulSoup to scrape web-pages
--------------------------------------

The bot uses the python lib `BeautifulSoup` to scrape information from webpages. Just to show it 
off how its done but it can of course be made into some useful stuff. 
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

Run `aggregate.php` from crontab with regular intervalls, for example each 5 minute.
  
    */5 * * * * /usr/local/bin/php /home/mos/git/irc2phpbb/aggregate.php

The id of the feed items are stored in a SQLite database to avoid duplicates being posted.


History
-------

Todo.

* Cache responses from smhi & sunrise services
* Add logfile entry containing current online users in the irc-channel


v0.2.x (latest) 

* Fixed loggin of ACTION.
* Logging as utf-8 to logfile in json format.
* Managing all strings as unicode internally.
* Improved encoding of incoming messages though `decode_irc`.
* Issues with irclog, utf8 and json encoding to file. debugging.


v0.2.1 (2012-05-14) 

* Corrected. Failed to decode utf-8 to json.


v0.2.0 (2012-05-13) 

* log all traffic in irc-channel to irclog.txt as json-encoded format.
* aggregate.php, remove duplicate post in same thread. Only show one.
* created functions sendMsg and sendPrivMsg to gather all output, reduce codelines and centralise 
  logging
* corrected that occasionally only sent one entry from the incoming directory thought it was more 
  to send.
* Make \r\n in central sendMsg() for each request


v0.1.0 (2012-02-14) 

* First tag after some live testing for a couple of months. Must start somewhere. 

 .   
..:  Copyright 2011 by Mikael Roos (me@mikaelroos.se)
