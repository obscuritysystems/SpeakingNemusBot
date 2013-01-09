import socket 
import sys
import time 
import httplib
from re import escape
from datetime import date


class Bot(object):
	
	host = ''
	channel = ''
	password = ''
	nicks  =''
	irc = ''
	debug = False
	loging = False

	def __init__(self,host,channel,password,nicks,host_name,debug,log):

		self.host = host
		self.channel = channel
		self.password = password
		self.nicks = nicks
		self.host_name = host_name
		self.debug = debug
		self.log= log

	def custom_ai(self,text,timestamp):
		pass
		#extend and put comst ai code here

	def tpars(self,txt):

		q=txt.split('<span class="temp">')[1]
		temp=q.split(' C')[0]
		qq=txt.split('<span>')[1]
		wind=qq.split('</span>')[0]

		return temp, wind

 	def parsemsg(self,s):
		"""Breaks a message from an IRC server into its prefix, command, and arguments."""
		try:
			prefix = ''
			trailing = []
			if not s:
				raise IRCBadMessage("Empty line.")
			if s[0] == ':':
				prefix, s = s[1:].split(' ', 1)

			if s.find(' :') != -1:
				s, trailing = s.split(' :', 1)
				args = s.split()
				args.append(trailing)
			else:
				args = s.split()
			command = args.pop(0)
				
			return {'channel':args[0],'handle':prefix.split('@')[0],'text':args[1]}

		except:
			return None
	
	def log_connectivity(self,text):
		pass
		
	def archive_message(self,text,timestamp):
		pass
		
	def sendm(self,msg): 
		text = 'PRIVMSG '+ self.channel + ' :' + str(msg) + '\r\n'
		if self.log:
			timestamp = int(time.time()) 
			self.archive_message(text,timestamp)
		self.irc.send(text)

	def bot_ai(self,text,timestamp):
	
		if text.find(':KICK') != 1:
			self.irc.send('JOIN '+ self.channel +'\r\n')
		
		if text.find(':!date') != -1:
			self.sendm('[+] Date: '+ time.strftime("%a, %b %d, %y", time.localtime()))
		
		if text.find(':!time') != -1:
			self.sendm('[+] Time: '+ time.strftime("%H:%M:%S", time.localtime()))
		
		if text.find(':!say') != -1:
			says = text.split(':!say')
			sayse = says[1].strip()
			self.sendm('.:: '+ str(sayse) +' ::.')
            
		if text.find(':!voice') != -1:
			voice = text.split(':!voice')
			voices = voice[1].strip()
			self.irc.send('MODE '+ str(channel) +' +v '+ str(voices) +'\r\n')

		if text.find(':!devoice') != -1:
			devoice = text.split(':!devoice')
			devoices = devoice[1].strip()
			self.irc.send('MODE '+ str(channel) +' -v '+ str(devoices) +'\r\n')
		
		
		if text.find(':!image') != -1:
			image = text.split(':!image')
			images = image[1].strip()
			if len(images) < 1:
				self.sendm('[+] Error ! Wrote : !image world')
			else:
				self.sendm('[+] images url : http://images.google.com/images?&q='+ images +'&btnG')
		
		if text.find(':!newyear') != -1:
			now = date.today()
			newyear = date(2009, 12, 31)
			cik = now - newyear
			newyears = cik.days
			self.sendm('[+] .. ...... .... ........ :'+ str(newyears) +' .... =)')
	
	def run(self):

		self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		self.irc.connect((self.host, 6667)) 

		self.irc.send('USER '+self.nicks+' host '+self.host_name+' : Nemus Brand Bot\r\n') 
		self.irc.send('NICK '+ str(self.nicks) +'\r\n')
		self.irc.send('NickServ IDENTIFY '+ str(self.nicks) + ' ' + str(self.password) +'\r\n')

		while 1:	

			try:
				text = self.irc.recv(2040)
				timestamp = int(time.time()) 
				if text.find('PRIVMSG') != -1 and self.log:
					self.archive_message(text,timestamp)
					self.log_connectivity(text)
				if not text:
					break

				if self.debug:
					print text
		
				if text.find('Message of the Day') != -1:
					self.irc.send('JOIN '+ self.channel +'\r\n')

				if text.find('+iwR') != -1:
					self.irc.send('NickServ IDENTIFY '+ str(self.nicks) + ' ' + str(self.password) +'\r\n')
                           
				if text.find('PING') != -1:
					print 'PONG ' + text.split() [1] + '\r\n'
					self.irc.send('PONG ' + text.split() [1] + '\r\n')

				self.bot_ai(text,timestamp)
				self.custom_ai(text,timestamp);

	
			except Exception, err:
				import traceback, os.path
				traceback.print_exc(err)
				print err
				pass
	
