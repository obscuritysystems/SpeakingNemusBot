#!/usr/bin/env python

import sys, time, socket
from daemon import Daemon
from speaok_bot_ai import SpeakBotAI

class SpeakBot(Daemon):

	def run(self):
		bot = SpeakBotAI()
		bot.run()
			

if __name__ == "__main__":
	daemon = NemusBot('/tmp/SpeakBot.pid')
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
