import os
import sqlite3 as lite
import sys
import ConfigParser
import time
	
class Talking(object):

	def __init__(self):

		self.running = True
		self.con = lite.connect('/tmp/speakbot.db')
		

	def run(self):
		

		while self.running:
			time.sleep(1)
			cur = self.con.cursor()
			cur.execute("select * from talk limit 1")
			rows = cur.fetchall()
			for row in rows:
				print row
				cur.execute("delete from talk where id = ?",(row[0],))
				self.con.commit()

		
			


talking = Talking()
talking.run()
