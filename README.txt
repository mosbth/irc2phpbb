An python implementation of an irc bot keeping track of latest posts in a phpbb forum.
Basic code from: http://osix.net/modules/article/?id=780 and http://oreilly.com/pub/h/1968
and developed from there.

The rfc for the irc protocol is quite helpful: http://www.irchelp.org/irchelp/rfc/

I'm using feedparser to parse the RSS feed.
http://wiki.python.org/moin/RssLibraries
http://code.google.com/p/feedparser/

The bot is (will be) active in irc://irc.bsnet.se/#db-o-webb which is a irc channel for 
teaching HTML, CSS, JavaScript, PHP, SQL and Unix. The forum is on http://dbwebb.se.

The file aggregate.php uses magpierss (http://magpierss.sourceforge.net/) to aggregate feeds from
several places and while discovering new entries it stores messages in the directory incoming
where Marvin (the bot) is looking, when finding a file there its content will be posted to the 
irc-channel by the bot itself.

Run aggregate.php from crontab with regulare intervalls, for example with each 5 minute intervall.
*/5 * * * * /usr/local/bin/php /home/mos/git/irc2phpbb/aggregate.php

The id of the feed items are stored in a SQLite database.


 .   
..:  Copyright 2011 by Mikael Roos (me@mikaelroos.se)
