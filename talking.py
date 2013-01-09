import os
import sqlite3 as lite
import sys
import ConfigParser
import time
import re
from daemon import Daemon
	
class TalkingDaemon(Daemon):

	def __init__(self,pid):
		super(TalkingDaemon,self).__init__(pid)
		self.running = True
		self.con = lite.connect('/tmp/speakbot.db')
		

	def run(self):
		

		while self.running:
			time.sleep(1)
			cur = self.con.cursor()
			cur.execute("select id,handle,channel,message from talk limit 1")
			rows = cur.fetchall()
			for row in rows:
				#print row
				speak = re.sub(r'[^\w]', ' ', row[3])
				print row
				cmd = 'espeak -s 130 "%s"'% speak
				print cmd
				cur.execute("delete from talk where id = ?",(row[0],))
				self.con.commit()

if __name__ == "__main__":

	daemon = TalkingDaemon('/tmp/speakbot_talking_deamon.pid')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)
		
			


