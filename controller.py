from re import findall
from requests import get
from json import loads,dumps
import sys, os, langlib1
import random

storage = {}
dictionary = {}
Authorized = ["u0CMoQl02f2b8a7cf5669f18d956f76c"]
updateDict = lambda : open("dict.json","w").write(dumps({"keywords":dictionary, "authorized":Authorized}))
myGuid = "u0DbDR404fa4978861008138e9616b8b"

def hasInsult(bot,msg): return any(word in open("dontReadMe.txt").read().split("\n") for word in msg.split())

def hasAds(bot, msg):
	links = list(map(lambda ID: ID.strip()[1:],findall(r"@[\w|_|\d]+", msg))) + list(map(lambda link:link.split("/")[-1],findall(r"rubika\.ir/\w+",msg)))
	joincORjoing = "joing" in msg or "joinc" in msg

	if joincORjoing: return joincORjoing
	else:
		for link in links:
			try:
				Type = bot.getInfoByUsername(link)["data"]["chat"]["abs_object"]["type"]
				if Type == "Channel": return True
			except KeyError: return False

def control(bot, target):
	try:
		global storage
		global dictionary
		group = bot.getGroupInfo(target)

		if not target in storage.keys():
			storage[target] = {
				"sleeped": False,
				"answered": []
			}

		if group["status"].upper()!="OK":
			storage.pop(target)
			return None
	
		while True:
			try:
				messages = bot.getMessages(target, group["data"]["chat"]["last_message_id"])
				GroupName = group["data"]["group"]["group_title"]
				admins = [i["member_guid"] for i in bot.getGroupAdmins(target)["data"]["in_chat_members"]]
				break
				#print(bot.getMessages(target, bot.getGroupInfo(target)["data"]["chat"]["last_message_id"]))
			except Exception as e: print(e)
	
	
		for msg in messages:
			print(msg)
			if msg["type"]=="Text" and not msg.get("message_id") in storage[target]["answered"] and msg["author_object_guid"] != myGuid:
				if not storage[target]["sleeped"]:
					if hasInsult(bot,msg["text"]) and not msg.get("author_object_guid") in admins :
						bot.deleteMessages(target, [str(msg.get("message_id"))])
		
					elif hasAds(bot,msg["text"]) and not msg.get("author_object_guid") in admins :
						bot.deleteMessages(target, [str(msg.get("message_id"))])
		
					elif "forwarded_from" in msg.keys() and bot.getMessagesInfo(target, [msg.get("message_id")])[0]["forwarded_from"]["type_from"] == "Channel" and not msg.get("author_object_guid") in admins :
						bot.deleteMessages(target, [str(msg.get("message_id"))])

					elif msg["text"].startswith("!joing") and msg.get("author_object_guid") in Authorized :
						bot.joinGroup(msg["text"].split()[1])

					elif msg["text"].startswith("!learn") and msg.get("author_object_guid") in Authorized :
						dictionary[bot.getMessagesInfo(target,[msg["reply_to_message_id"]])[0]["text"]] = " ".join(msg["text"].split()[1:])
						#open("dict.json","w").write(dumps({"keywords":dictionary, "authorized":Authorized}))
						bot.sendMessage(target, "done 🤓", message_id=msg.get("message_id"))

					elif msg["text"].startswith("!authorize") and msg["author_object_guid"] == Authorized[0] :
						Authorized.append(msg["text"].split()[1])
						#open("dict.json","w").write(dumps({"keywords":dictionary, "authorized":Authorized}))

					elif msg["text"].startswith("!unauthorize") and msg["author_object_guid"] == Authorized[0] :
						Authorized.remove(msg["text"].split()[1])
						#open("dict.json","w").write(dumps({"keywords":dictionary, "authorized":Authorized}))

					elif msg["text"] in dictionary.keys() :
						exec(dictionary[msg["text"]])
						#bot.sendMessage(target, dictionary[msg["text"]], message_id=msg.get("message_id"))
		
					elif msg["text"] == "!sleep" and msg.get("author_object_guid") in admins :
						storage[target]["sleeped"] = True
						bot.sendMessage(target, "🛌", message_id=msg.get("message_id"))
		
					elif msg["text"] == "!del" and msg.get("author_object_guid") in admins :
						bot.deleteMessages(target, [msg.get("reply_to_message_id")])
						bot.deleteMessages(target, [msg["message_id"]])
						bot.sendMessage(target, "✅", message_id=msg.get("message_id"))
		
					elif msg["text"].startswith("!ban") and msg.get("author_object_guid") in admins :
						try:
							guid = bot.getInfoByUsername(msg["text"].split(" ")[1][1:])["data"]["chat"]["abs_object"]["object_guid"]
							if not guid in admins :
								bot.banGroupMember(target, guid)
								bot.sendMessage(target, "✅", message_id=msg.get("message_id"))
							else :
								bot.sendMessage(target, "❎", message_id=msg.get("message_id"))
		
						except IndexError:
							guid = bot.getMessagesInfo(target, [msg.get("reply_to_message_id")])[0]["author_object_guid"]
							if not guid in admins:
								bot.banGroupMember(target, guid)
								bot.sendMessage(target, "✅", message_id=msg.get("message_id"))
							else :
								bot.sendMessage(target, "❎", message_id=msg.get("message_id"))
		
					elif msg["text"].startswith("!add") :
						bot.invite(target, [bot.getInfoByUsername(msg["text"].split()[1][1:])["data"]["chat"]["object_guid"]])
						bot.sendMessage(target, "✅", message_id=msg.get("message_id"))
		
					elif msg["text"] == "!lock" and msg.get("author_object_guid") in admins :
						bot.setMembersAccess(target, ["AddMember"]).text
						bot.sendMessage(target, "🔒", message_id=msg.get("message_id"))
		
					elif msg["text"] == "!unlock" :
							bot.setMembersAccess(target, ["ViewMembers","ViewAdmins","SendMessages","AddMember"])
							bot.sendMessage(target, "🔓", message_id=msg.get("message_id"))
		
					elif msg["text"] == "!list" :
						bot.sendMessage(target, f'''دستورات ربات {GroupName} 🤖
	
	🌟 برای ادمین ها 🌟
	!ban <حذف کاربر 👉 <ریپلای
	!ban <حذف کاربری 👉 <نام کاربری
	!del <حذف پیام 👉 <ریپلای
	!lock 👉 قفل کردن گروه
	!unlock 👉 باز کردن گروه
	!sleep 👉 ایجاد وقفه در اجرای ربات
	!wakeup 👉 حذف وقفه
	!setTimer <sec> 👉 تنظیم تایمر
	!pin <reply> 👉 سنجاق کردن پیام
	!unpin <reply> 👉 درآوردن پیام از سنجاق
	
	👤 برای کاربران 👤
	!add <افزودن کاربر 👉 <نام کاربری
	!rank <ترافیک جستجوی سایت 👉 <لینک
	!short <کوتاه کردن لینک 👉 <لینک
	!font <زیبا کردن نام شما 👉 <نام
	!link 👉 دریافت لینک گروه
	!list 👉 مشاهده این پیام
	!webshot <URL.ir> 👉 اسکرین شات از سایت
		
	‼️ نکته ‼️
	فوروارد از کانال، ارسال لینک کانال یا گروه و ارسال فحش، چنانچه از سمت ادمین نباشد توسط ربات حذف می‌شود.
	''',metadata=[{"from_index":0, "length": 7, "type": "Bold"}],message_id=msg["message_id"])
		
					elif msg["text"].startswith("!rank"):
						bot.sendMessage(target, "🔍 ترافیک جستجو : "+get(f"https://api.codebazan.ir/alexa/index.php?url={msg['text'].split()[1]}").json()["COMPARISON-METRICS"]["Search-Traffic"], message_id=msg["message_id"])
		
		
					elif msg["text"].startswith("!short"):
						bot.sendMessage(target, "🔗 "+get(f"https://rizy.ir/api?api=64f7450caf6800c3d29f3f627137ebc65b1828b2&url={msg['text'].split()[1]}").json()["shortenedUrl"], message_id=msg["message_id"])
		
					elif msg["text"].startswith("!font"):
						try:
							#print("\n".join(list(response["result"].values())))
							response = get(f"https://api.codebazan.ir/font/?text={'%20'.join(msg['text'].split()[1:])}").json()
							bot.sendMessage(msg["author_object_guid"], "\n".join(list(response["result"].values())[:90])).text
							bot.sendMessage(target, "نتیجه به پیوی شما ارسال شد ✅", message_id=msg["message_id"])
						except Exception as e:
							print(e)
							bot.sendMessage(target, "متأسفانه نتیجه‌ای در بر نداشت ☹️", message_id=msg["message_id"])
		
					elif msg["text"] == "!link":
						bot.sendMessage(target, bot.getGroupLink(target), message_id=msg["message_id"])
		
					elif msg["text"].startswith("!webshot"):
						try:
							args = msg['text'].split()[1]
							if '.ir' in args:
								response = get(f"https://api.codebazan.ir/webshot/?text=1000&domain={args}").content
							else:
								response = get("https://http.cat/403").content
							with open("shot.jpg","wb") as shot: shot.write(response)
							bot.sendPhoto(target, "./shot.jpg", [720,720], caption="نمایی از صفحه موردنظر شما", message_id=msg["message_id"])
						except: bot.sendMessage(target, "متأسفانه نتیجه‌ای در بر نداشت ☹️", message_id=msg["message_id"])
	
					elif msg["text"] == "!pin" and msg.get("author_object_guid") in admins and "reply_to_message_id" in list(msg.keys()) :
						bot.pin(target, msg["reply_to_message_id"])
		
					elif msg["text"] == "!unpin" and msg.get("author_object_guid") in admins and "reply_to_message_id" in list(msg.keys()) :
						bot.unpin(target, msg["reply_to_message_id"])
						bot.sendMessage(target, "✅", message_id=msg["message_id"])
		
					elif msg["text"].startswith("!setTimer") and msg.get("author_object_guid") in admins :
						loads(bot.enc.decrypt(bot.setGroupTimer(target, int(msg["text"].split()[1])).json()["data_enc"]))
						bot.sendMessage(target, f"⏱️ -> {(msg['text'].split()[1])}s", message_id=msg["message_id"])
	
		
					elif msg["text"].startswith("!say"):
						text = " ".join(msg["text"].split()[1:])
						langlib1.TTS(text, False, f"./{msg['message_id']}.ogg")
						bot.sendVoice(target, f"./{msg['message_id']}.ogg", 1000, caption=text, message_id=msg["message_id"])

				else:
					if msg["text"] == "!wakeup" and msg.get("author_object_guid") in admins :
						storage[target]["sleeped"] = False
						bot.sendMessage(target, "🛏️", message_id=msg.get("message_id"))
	
			elif msg["type"]=="Event" and not msg.get("message_id") in storage[target]["answered"] and not storage[target]["sleeped"]:
				data = msg['event_data']
				if data["type"]=="RemoveGroupMembers":
					user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
					bot.sendMessage(target, f"بای بای {user} 🗑️", message_id=msg["message_id"])
		
				elif data["type"]=="AddedGroupMembers":
					user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
					bot.sendMessage(target, f"سلام {user} عزیز به گروه {GroupName} خوش اومدی 😃\nلطفا قوانین رو رعایت کن 🥰", message_id=msg["message_id"])
		
				elif data["type"]=="LeaveGroup":
					user = bot.getUserInfo(data['performer_object']['object_guid'])["data"]["user"]["first_name"]
					bot.sendMessage(target, f"بای بای {user} 🗑️", message_id=msg["message_id"])
		
				elif data["type"]=="JoinedGroupByLink":
					user = bot.getUserInfo(data['performer_object']['object_guid'])["data"]["user"]["first_name"]
					bot.sendMessage(target, f"سلام {user} عزیز به گروه {GroupName} خوش اومدی 😃\nلطفا قوانین رو رعایت کن 🥰", message_id=msg["message_id"])
	
			storage[target]["answered"].append(msg["message_id"])

	except KeyboardInterrupt:
		exit()