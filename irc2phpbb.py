#! /usr/bin/env python
# -*- coding: utf-8 -*-

#import some stuff
import sys 
import socket 
import string 
import random 
import os #not necassary but later on I am going to use a few features from this 
import feedparser # http://wiki.python.org/moin/RssLibraries
import shutil
import codecs
from collections import deque
from datetime import datetime
import re
import urllib2
from bs4 import BeautifulSoup
import time
import json

import phpmanual

# Local module file
#import fix_bad_unicode


#
# Settings
#
HOST='irc.bsnet.se' 			# The server we want to connect to 
PORT=6667 								# The connection port which is usually 6667 
NICK='marvin' 						# The bot's nickname 
IDENT='somepass'         # Password to identify for nick
REALNAME='Mr Marvin Bot' 
OWNER='thebiffman' 							# The bot owner's nick 
CHANNEL='#db-o-webb'      # The default channel for the bot 
#CHANNEL='#db-o-webb-test'      # The default channel for the bot 
INCOMING='incoming'			  # Directory for incoming messages 
DONE='done'			  				# Directory to move all incoming messages once processed
readbuffer='' 						# Here we store all the messages from server 
HOME='https://github.com/mosbth/irc2phpbb'
FEED_FORUM='http://dbwebb.se/forum/feed.php'
# FEED_LISTEN='http://ws.audioscrobbler.com/1.0/user/mikaelroos/recenttracks.rss'
FEED_LISTEN='http://ws.audioscrobbler.com/1.0/user/djazzradio/recenttracks.rss'

SMHI_PROGNOS='http://www.smhi.se/vadret/vadret-i-sverige/Vaderoversikt-Sverige-meteorologens-kommentar?meteorologens-kommentar=http%3A%2F%2Fwww.smhi.se%2FweatherSMHI2%2Flandvader%2F.%2Fprognos15_2.htm'
#SUNRISE='http://www.timeanddate.com/astronomy/sweden/jonkoping' Stopped working
SUNRISE='http://www.timeanddate.com/sun/sweden/jonkoping'

LOGFILE='irclog.txt'        # Save a log with latest messages
LOGFILEMAX=20
irclog=deque([],LOGFILEMAX) # Keep a log of the latest messages


#
# Manage character encoding issues for incoming messages
# http://stackoverflow.com/questions/938870/python-irc-bot-and-encoding-issue
#
def decode_irc(raw, preferred_encs = ["UTF-8", "CP1252", "ISO-8859-1"]):
  changed = False
  for enc in preferred_encs:
    try:
      res = raw.decode(enc)
      changed = True
      break
    except:
      pass
  if not changed:
    try:
      enc = chardet.detect(raw)['encoding']
      res = raw.decode(enc)
    except:
      res = raw.decode(enc, 'ignore')
  return res



#
#Function to parse incoming messages
#
def parsemsg(msg): 
	complete=msg[1:].split(':',1) #Parse the message into useful data 
	info=complete[0].split(' ') 
	msgpart=complete[1] 
	sender=info[0].split('!') 
	if msgpart[0]=='`' and sender[0]==OWNER: #Treat all messages starting with '`' as command 
		cmd=msgpart[1:].split(' ') 
		if cmd[0]=='op': 
			s.send('MODE '+info[2]+' +o '+cmd[1]+'n') 
		if cmd[0]=='deop': 
			s.send('MODE '+info[2]+' -o '+cmd[1]+'n') 
		if cmd[0]=='voice': 
			s.send('MODE '+info[2]+' +v '+cmd[1]+'n') 
		if cmd[0]=='devoice': 
			s.send('MODE '+info[2]+' -v '+cmd[1]+'n') 
		if cmd[0]=='sys': 
			syscmd(msgpart[1:],info[2]) 
			 
	if msgpart[0]=='-' and sender[0]==OWNER : #Treat msgs with - as explicit command to send to server 
		cmd=msgpart[1:] 
		s.send(cmd+'n') 
		print 'cmd='+cmd 


#This piece of code takes the command and executes it printing the output to ot.txt. Then ot.txt is 
#read and displayed to the given channel. Multiline output is shown by using '|'. 
def syscmd(commandline,channel): 
    cmd=commandline.replace('sys ','') 
    cmd=cmd.rstrip() 
    os.system(cmd+' >temp.txt') 
    a=open('temp.txt') 
    ot=a.read() 
    ot.replace('n','|') 
    a.close() 
    s.send('PRIVMSG '+channel+' :'+ot+'n') 
    return 0 


# Send and occasionally print the message sent.
def sendMsg(s, msg):
  print(msg.rstrip('\r\n'))
  s.send(msg)


# Send and log a PRIV message
def sendPrivMsg(s, msg):
  global irclog
  irclog.append({'time':datetime.now().strftime("%H:%M").rjust(5), 'user':NICK.ljust(8), 'msg':msg})
  #irclog.append("%s %s %s" % (datetime.now().strftime("%H:%M").rjust(5), NICK.ljust(8), msg))
  print "PRIVMSG %s :%s\r\n" % (CHANNEL, msg)
  sendMsg(s,"PRIVMSG %s :%s\r\n" % (CHANNEL, msg))


#Read all files in the directory incoming, send them as a message if they exists and then move the
#file to directory done.
def readincoming(dir): 
	listing = os.listdir(dir)
	for infile in listing:
		filename=dir + '/' + infile
		#text=codecs.open(filename, 'r', 'utf-8').read()
		text=file(filename).read()
		msg="PRIVMSG %s :%s\r\n" % (CHANNEL, text)
		sendMsg(s,msg)
		try:
			shutil.move(filename, DONE)
		except Exception:
			os.remove(filename)
			

#Connect 
#Create the socket  & Connect to the server
s=socket.socket( ) 																		
print "Connecting: %s:%d" % (HOST, PORT)
s.connect((HOST, PORT)) 

#Send the nick to server 
sendMsg(s,'NICK %s\r\n' % NICK)

#Identify to server 
sendMsg(s,'USER  %s %s dbwebb.se :%s\r\n' % (NICK, HOST, REALNAME))

#This is my nick, i promise!
sendMsg(s,'PRIVMSG nick IDENTIFY %s\r\n' % IDENT)

#Join a channel 
sendMsg(s,'JOIN %s\r\n' % CHANNEL)


#Wait and listen
#We recieve the server input in a variable line; if you want to see the servers messages, 
#use print line. Once we connect to the server, we join a channel. Now whenever we recieve 
#any PRIVMSG, we call a function which does the appropriate action. The next few lines are 
#used to reply to a servers PING. Until this point, the bot just sits idle in a channel. 
#To make it active we use the parsemsg function. 
#PRIVMSG are usually of this form: 
# :nick!username@host PRIVMSG channel/nick :Message 
msgs=['Ja, vad kan jag göra för Dig?', 'Låt mig hjälpa dig med dina strävanden.', 'Ursäkta, vad önskas?', 
'Kan jag stå till din tjänst?', 'Jag kan svara på alla dina frågor.', 'Ge me hög-fem!',
'Jag svarar endast inför thebiffman, det är min enda herre.', 'thebiffman är kungen!',
'Oh, ursäkta, jag slumrade visst till.', 'Fråga, länka till kod och source.php och vänta på svaret.']

hello=['Hej själv! ', 'Trevligt att du bryr dig om mig. ', 'Det var länge sedan någon var trevlig mot mig. ', 
'Halloj, det ser ut att bli mulet idag. ',
]

smile=[':-D', ':-P', ';-P', ';-)', ':-)', '8-)']

lunch=['ska vi ta boden uppe på parkeringen idag? en pasta, ris eller kebabrulle?', 
'ska vi dra ned till den indiska och ta en 1:a, den är stark o fin, man får ju bröd också.', 
'thairestaurangen var inte så dum borta vid korsningen.', 
'jag har med mig en matlåda hemmifrån så det är lugnt idag.', 
'ska vi chansa och ta BTH-fiket? kan ju ta en färdig sallad om inte annat...', 
'det är lite mysigt i fiket jämte demolabbet, där kan man hitta något enkelt.',
'jag bantar så jag ligger lågt med maten idag. måste ha lite koll på vikten.']

quote=['I could calculate your chance of survival, but you won\'t like it.', 
'I\'d give you advice, but you wouldn\'t listen. No one ever does.', 
'I ache, therefore I am.', 
'I\'ve seen it. It\'s rubbish. (About a Magrathean sunset that Arthur finds magnificent)', 
'Not that anyone cares what I say, but the Restaurant is on the other end of the universe.', 
'I think you ought to know I\'m feeling very depressed.',
'My capacity for happiness," he added, "you could fit into a matchbox without taking out the matches first.',
'Arthur: "Marvin, any ideas?" Marvin: "I have a million ideas. They all point to certain death."',
'"What\'s up?" [asked Ford.] "I don\'t know," said Marvin, "I\'ve never been there."',
'Marvin: "I am at a rough estimate thirty billion times more intelligent than you. Let me give you an example. Think of a number, any number." Zem: "Er, five." Marvin: "Wrong. You see?"',
'Zaphod: "Can it Trillian, I\'m trying to die with dignity. Marvin: "I\'m just trying to die."']

lyssna=['Jag gillar låten', 'Senaste låten jag lyssnade på var', 'Jag lyssnar just nu på',
'Har du hört denna låten :)', 'Jag kan tipsa om en bra låt ->']

attack=['Aaaaarrggh mateys! You will walk the plank!', 
'Nej, jag orkar inte =(', 
'Yippee-ki-yay, motherf*cker!', 
'DEAAAAAAAAAAATH!', 
'You\'re in for a world of pain', 
'For the Horde!', 
'The Almighty tells me he can get me out of this mess, but he\'s pretty sure you\'re fuc*ed.',
'There\'s nothing stronger than the heart of a volunteer.']

slaps=[' in the face with a rotten old fish.',
' around a bit with a large trout.',
' in the face with a keyboard.',
' around with a glove.',
' over the head with a fluffy pillow.',
' about the head and shoulders with a rubber chicken.',
' with a large squid... I hope you like seafood.',
' about the head and shoulders with a rubber chicken.'
]


#
# Main loop
#
while 1: 
  json.dump(list(irclog), file(LOGFILE, 'w'), False, False, False, False, indent=2) #Write IRC to logfile
  readincoming(INCOMING)
  readbuffer=readbuffer+s.recv(1024)
  temp=string.split(readbuffer, "\n")
  readbuffer=temp.pop( )
  
  for line in temp:
    line = decode_irc(line)
    #print "HERE %s" % (line.encode('utf-8', 'ignore'))

    line=string.rstrip(line)
    line=string.split(line)
    row=' '.join(line[3:]).replace(':',' ').replace(',',' ').replace('.',' ').replace('?',' ').strip().lower()
    row=row.split()
    print "%s" % (line)
    #print "%s" % (row)
  
    if line[0]=="PING":
      sendMsg(s,"PONG %s\r\n" % line[1])
    
    if line[1]=='PRIVMSG' and line[2]==CHANNEL:
      if line[3]==u':\x01ACTION':
        irclog.append({'time':datetime.now().strftime("%H:%M").rjust(5), 'user':'* ' + re.search('(?<=:)\w+', line[0]).group(0).encode('utf-8', 'ignore'), 'msg':' '.join(line[4:]).lstrip(':').encode('utf-8', 'ignore')}) 
      else:
        #irclog.append({'time':datetime.now().strftime("%H:%M").rjust(5), 'user':re.search('(?<=:)\w+', line[0]).group(0).ljust(8), 'msg':' '.join(line[3:]).lstrip(':')}) 
        #irclog.append({'time':datetime.now().strftime("%H:%M").rjust(5), 'user':re.search('(?<=:)\w+', line[0]).group(0).encode('utf-8', 'ignore'), 'msg':' '.join(line[3:]).lstrip(':').encode('utf-8', 'ignore')}) 
        irclog.append({'time':datetime.now().strftime("%H:%M").rjust(5), 'user':re.search('(?<=:)\w+', line[0]).group(0).encode('utf-8', 'ignore'), 'msg':' '.join(line[3:]).lstrip(':').encode('utf-8', 'ignore')}) 
        #(datetime.now().strftime("%H:%M").rjust(5), re.search('(?<=:)\w+', line[0]).group(0).ljust(8), ' '.join(line[3:]).lstrip(':'))) 

    if line[1]=='PRIVMSG' and line[2]==CHANNEL and NICK in row:
      if 'lyssna' in row or 'lyssnar' in row or 'musik' in row:
        feed=feedparser.parse(FEED_LISTEN)
        sendPrivMsg(s,"%s %s" % (lyssna[random.randint(0,len(lyssna)-1)], feed["items"][0]["title"].encode('utf-8', 'ignore')))
      elif ('latest' in row or 'senaste' in row or 'senast' in row) and ('forum' in row or 'forumet' in row):
        feed=feedparser.parse(FEED_FORUM)
        sendPrivMsg(s,"Forumet: \"%s\" av %s http://dbwebb.se/f/%s" % (feed["items"][0]["title"].encode('utf-8', 'ignore'), feed["items"][0]["author"].encode('utf-8', 'ignore'), re.search('(?<=p=)\d+', feed["items"][0]["id"].encode('utf-8', 'ignore')).group(0)))
      elif 'smile' in row or 'le' in row or 'skratta' in row or 'smilies' in row:
        sendPrivMsg(s,"%s" % (smile[random.randint(0,len(smile)-1)]))
      elif unicode('källkod', 'utf-8') in row or 'source' in row:
        sendPrivMsg(s,"I PHP-kurserna kan du länka till source.php. Annars fungerar sidor som pastebin bra. Om man vill kunna ändra på koden efter den är uppladdad  är www.codeshare.io en bra sida.")
      elif ('budord' in row or 'stentavla' in row) and ('1' in row or '#1' in row):
        sendPrivMsg(s,"Ställ din fråga, länka till exempel och source.php. Häng kvar och vänta på svar.")
      elif ('budord' in row or 'stentavla' in row) and ('2' in row or '#2' in row):
        sendPrivMsg(s,"Var inte rädd för att fråga och fråga tills du får svar: http://dbwebb.se/f/6249")
      elif ('budord' in row or 'stentavla' in row) and ('3' in row or '#3' in row):
        sendPrivMsg(s,"Öva dig ställa smarta frågor: http://dbwebb.se/f/7802")
      elif ('budord' in row or 'stentavla' in row) and ('4' in row or '#4' in row):
        sendPrivMsg(s,"When in doubt - gör ett testprogram. http://dbwebb.se/f/13570")
      elif ('budord' in row or 'stentavla' in row) and ('5' in row or '#5' in row):
        sendPrivMsg(s,"Hey Luke - use the source! http://catb.org/jargon/html/U/UTSL.html")
      elif 'lunch' in row or 'mat' in row or unicode('äta', 'utf-8') in row:
        sendPrivMsg(s,"%s" % (lunch[random.randint(0,len(lunch)-1)]))
      elif 'quote' in row or 'citat' in row or 'filosofi' in row or 'filosofera' in row:
        sendPrivMsg(s,"%s" % (quote[random.randint(0,len(quote)-1)]))
      elif 'hem' in row or (('vem' in row or 'vad' in row) and (unicode('är', 'utf-8') in row)):
        sendPrivMsg(s,"Jag är en tjänstvillig själ som gillar webbprogrammering. Jag bor på github: %s och du kan diskutera mig i forumet http://dbwebb.se/forum/viewtopic.php?f=21&t=20"  % (HOME))
      elif unicode('hjälp', 'utf-8') in row or 'help' in row:
        sendPrivMsg(s,"[ vem är | forum senaste | lyssna | le | lunch | citat | budord 1 (2, 3, 4, 5) | väder | solen | hjälp | * * ]")
      elif unicode('väder', 'utf-8') in row or unicode('vädret', 'utf-8') in row or 'prognos' in row or 'prognosen' in row or 'smhi' in row:
        soup = BeautifulSoup(urllib2.urlopen(SMHI_PROGNOS))
        sendPrivMsg(s,"%s. %s. %s" % (soup.h1.text.encode('utf-8', 'ignore'), soup.h4.text.encode('utf-8', 'ignore'), soup.h4.findNextSibling('p').text.encode('utf-8', 'ignore')))
      elif 'sol' in row or 'solen' in row or unicode('solnedgång', 'utf-8') in row or unicode('soluppgång', 'utf-8') in row:
        try:
          soup = BeautifulSoup(urllib2.urlopen(SUNRISE))
          spans = soup.find_all("span", { "class" : "three" })
          sunrise = spans[0].text.encode('utf-8', 'ignore')
          sunset = spans[1].text.encode('utf-8', 'ignore')
          sendPrivMsg(s,"Idag går solen upp %s och ner %s. Iallafall i trakterna kring Jönköping." % (sunrise, sunset))
        except:
          sendPrivMsg(s,"Jag hittade tyvär inga solar idag :(")

        #div = soup.find(id="qfacts")
        #sunrise = div.p.next_sibling.span.next_sibling.text.encode('utf-8', 'ignore')
        #sunset = div.p.next_sibling.p.br.span.next_sibling.text.encode('utf-8', 'ignore')
        #endPrivMsg(s,"Idag går solen upp %s och ner %s. Iallafall i trakterna kring Jönköping." % (sunrise, sunset))

      elif unicode('snälla', 'utf-8') in row or 'hej' in row or 'tjena' in row or 'morsning' in row  or unicode('mår', 'utf-8') in row  or unicode('hallå', 'utf-8') in row or 'hallo' in row or unicode('läget', 'utf-8') in row or unicode('snäll', 'utf-8') in row or 'duktig' in row  or unicode('träna', 'utf-8') in row  or unicode('träning', 'utf-8') in row  or 'utbildning' in row or 'tack' in row or 'tacka' in row or 'tackar' in row or 'tacksam' in row:
        sendPrivMsg(s,"%s %s %s" % (smile[random.randint(0,len(smile)-1)], hello[random.randint(0,len(hello)-1)], msgs[random.randint(0,len(msgs)-1)]))
      elif 'attack' in row:
        sendPrivMsg(s,"%s" % (attack[random.randint(0,len(attack)-1)]))
      elif 'upprop' in row:
        sendPrivMsg(s, "Titta vad jag hittade: 3v upprop vårterminen 2015 - http://dbwebb.se/forum/viewtopic.php?f=30&t=3613")
      elif 'stats' in row or 'ircstats' in row:
        sendPrivMsg(s, "Statistik för kanalen finns här: http://dbwebb.se/irssistats/db-o-webb.html")
      elif 'slap' in row:
        #print('\r\nSlap!\r\n')
        if len(row) >= 3 and row[1] == 'slap':
          sendPrivMsg(s, "\001ACTION slaps " + row[2] + slaps[random.randint(0,len(slaps)-1)] + "\001")
      elif 'php' in row:
        if len(row) >= 3 and row[1] == 'php':
          function = row[2].encode('utf-8', 'ignore')
          result = phpmanual.getShortDescr(function)
          sendPrivMsg(s, result)
