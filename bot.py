from rubika.client import Bot
from rubika.tools import Tools
import sys, os
from controller import control
from threading import Thread

bot = Bot("xbiuifzcwcuypxidalxvdmwugkojofjh")
again = []

while True:
	try:
		#print(bot.getChatsUpdate())
		groups = [i["object_guid"] for i in bot.getChatsUpdate() if i["object_guid"].startswith("g")]
		print(groups)
		for gp in groups:
			control(bot, gp)
			# if not gp in again:
			# 	Thread(target=control,args=(bot,gp)).start()
			# 	again.append(gp)
			#Thread(target=control,args=(bot,gp)).start()
		'''
		targets = {}
		runnedTreads = []
		#print(bot.getChatsUpdate())
		print(groups)
		for target in groups:
			if not target in targets.keys():
				targets[target] = Thread(target=control,args=(bot,target))

		for i in targets.keys():
			thread = targets[i]
			if not thread in runnedTreads:
				runnedTreads.append(thread)
				thread.start()

		print(runnedTreads)
		'''
	
	except KeyboardInterrupt:
		exit()

	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)