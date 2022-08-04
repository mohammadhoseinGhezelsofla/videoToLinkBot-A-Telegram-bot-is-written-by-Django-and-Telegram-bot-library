from telegram import Bot, Update
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from .models import User, getUser
from .extractor import extractYoutubePlaylist, extractAparatPlaylist
import traceback

class botApi(Bot):
	def __init__(self, token) -> None:
		return super().__init__(token=token)
	def sendMessage(self, userId, message, removeMarkup=True):
		self.send_message(userId, message)

	def isYoutubePlaylistLink(self, s: str):
		if "youtube.com/playlist?list=" in s: return True
		return False

	def isAparatPlaylistLink(self, s: str):
		if "aparat.com/playlist/" in s: return True
		return False

	def handle(self, updates):
		for update in updates:
			if update.message:
				userId=update.effective_chat.id
				user=getUser(userId)
				text=update.effective_message.text
				messageId=update.effective_message.message_id
				if text=="/start":
					if user:
						user.delete()
					User(userId=userId, firstname=update.message.from_user.first_name, lastname=update.message.from_user.last_name).save()
					self.send_message(userId, text='سلام!\nخوش اومدی!\nمیتونی یک لینک playlist از youtube یا aparat رو برای من بفرستی تا من لینک تک تک track های اونو بهت بدم و تو هم بتونی با دانلود منیجرت بدون فیلترشکن دانلودشون کنی! پس منتظر چی هستی! امتحان کن!')
				elif self.isAparatPlaylistLink(text):
					pid=text.split('/playlist/')[1].split('/')[0]
					kb=[]
					kb.append(InlineKeyboardButton("144p", callback_data=f"aplink,{pid},144p"))
					kb.append(InlineKeyboardButton("240p", callback_data=f"aplink,{pid},240p"))
					kb.append(InlineKeyboardButton("360p", callback_data=f"aplink,{pid},360p"))
					kb.append(InlineKeyboardButton("480p", callback_data=f"aplink,{pid},480p"))
					self.send_message(chat_id=userId, text='لطفا کیفیت دانلود ترک ها را انتخاب کن', reply_markup=InlineKeyboardMarkup([kb]), reply_to_message_id=messageId)
					user.save()
				elif self.isYoutubePlaylistLink(text):
					pid=text.split("list=")[1].split("&")[0]
					kbv=[]
					kbv.append(InlineKeyboardButton("mp4 360p", callback_data=f"ytlink,{pid},18"))
					kbv.append(InlineKeyboardButton("mp4 720p", callback_data=f"ytlink,{pid},22"))
					kbv.append(InlineKeyboardButton("mp4 1080p", callback_data=f"ytlink,{pid},37"))
					kbv.append(InlineKeyboardButton("mp4 3072p", callback_data=f"ytlink,{pid},38"))
					kba=[]
					kba.append(InlineKeyboardButton("m4a 128kbps", callback_data=f"ytlink,{pid},140"))
					kba.append(InlineKeyboardButton("m4a 256kbps", callback_data=f"ytlink,{pid},141"))
					self.send_message(chat_id=userId, text='لطفا کیفیت دانلود ترک ها را انتخاب کن', reply_markup=InlineKeyboardMarkup([kbv, kba]), reply_to_message_id=messageId)
				else:
					self.send_message(userId, text="پیام معتبر نیست", reply_to_message_id=messageId, reply_markup=ReplyKeyboardRemove())
			elif update.callback_query:
				mode, pid, quality=update.callback_query.data.split(',')
				if mode=="aplink":
					if extractAparatPlaylist(pid, quality, update, self)==False: update.callback_query.edit_message_text("مشکلی در هنگام پردازش لینک پیش آمد. لطفا مجدد امتحان کنید")
				elif mode=="ytlink":
					if extractYoutubePlaylist(pid, quality, update, self)==False: pass#update.callback_query.edit_message_text("مشکلی در هنگام پردازش لینک پیش آمد. لطفا مجدد امتحان کنید")
