from bot import Bot
import re
import time 
import ConfigParser
import sqlite3 as lite
import sys

class SpeakBotAI(Bot):

	def __init__(self):
		
		config = ConfigParser.RawConfigParser()
		config.read('speak_bot.cfg')	

		host 		= config.get('Bot','host')
		channel 	= config.get('Bot','channel')
		password 	= config.get('Bot','password')
		nicks 		= config.get('Bot','nicks') 
		hostname 	= config.get('Bot','hostname')
		debug 		= config.getboolean('Bot','debug')
		log 		= config.getboolean('Bot','log')

		self.con = lite.connect('/tmp/speakbot.db')
		cur = self.con.cursor()
		cur.execute("create TABLE if not exists talk ( id INTEGER PRIMARY KEY AUTOINCREMENT, handle TEXT, channel TEXT , message TEXT)")
		self.con.commit()
		
		self.logged_in = False

		super(SpeakBotAI,self).__init__(host,channel,password,nicks,hostname,debug,log)
	

	def log_connectivity(self,text):
		pass
	
	def archive_message(self,text,timestamp):
		pass

	def custom_ai(self,text,timestamp):
		
	 	parsed_msg = self.parsemsg(text)

		if parsed_msg is not None:

			if text.find('SpeakBot @ ' + self.channel) != -1:
				self.logged_in = True

			if self.logged_in:
				cur = self.con.cursor()
				cur.execute('INSERT INTO talk(handle,channel,message) values (?,?,?)',(parsed_msg['handle'],parsed_msg['text'],parsed_msg['channel']))
				self.con.commit()

bot = SpeakBotAI()
bot.run()
