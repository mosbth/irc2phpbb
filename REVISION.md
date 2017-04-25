REVISION HISTORY
==================

Todo.

* Not using revision history correctly, perhaps clean it up or something like that...
* Cache responses from smhi & sunrise services
* Add logfile entry containing current online users in the irc-channel


v0.3.2 (2017-04-25)
-------------------

* Before mergin PR #33.
* Moved revision history to own file.


v0.3.1 (2015-12-16)
-------------------

* Use travis for tests.
* Add pylint and jsonlint.
* Fix crash on smhi wrong url.
* Added comic strips from commitStrip.
* Fixed crash on mondays, #9.
* Moved all strings to `marvin_strings.json`.
* Improving documentation.


v0.3.0 (2015-04-24) 
-------------------

* Major rewrite to python3 and separating code into modules.


v0.2.2 (2015-04-24) 
-------------------

* Fixed loggin of ACTION.
* Logging as utf-8 to logfile in json format.
* Managing all strings as unicode internally.
* Improved encoding of incoming messages though `decode_irc`.
* Issues with irclog, utf8 and json encoding to file. debugging.


v0.2.1 (2012-05-14) 
-------------------

* Corrected. Failed to decode utf-8 to json.


v0.2.0 (2012-05-13) 
-------------------

* log all traffic in irc-channel to irclog.txt as json-encoded format.
* aggregate.php, remove duplicate post in same thread. Only show one.
* created functions sendMsg and sendPrivMsg to gather all output, reduce codelines and centralise 
  logging
* corrected that occasionally only sent one entry from the incoming directory thought it was more 
  to send.
* Make \r\n in central sendMsg() for each request


v0.1.0 (2012-02-14) 
-------------------

* First tag after some live testing for a couple of months. Must start somewhere. 
