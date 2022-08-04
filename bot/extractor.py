from datetime import timedelta
import time
import requests
from json import loads
from jsonpath_ng import parse
from jsonpath_ng.ext import parser
from telegram import Bot, Update
from os import remove
import traceback

class playlist:
	def __init__(self, tracks, data):
		self.tracks=tracks
		self.data=data
	def __getattr__(self, name):
		if name in self.data: return self.data[name]
		return ''
	def next(self):
		pass


def toTime(seconds):
	if isinstance(seconds, str):
		seconds=int(seconds)
	d=str(timedelta(seconds=seconds)).split(':')
	if len(d)>2:
		return d[0]+' ساعت، '+d[1]+' دقیقه و '+d[2]+' ثانیه'
	elif len(d)>1:
		return d[0]+' دقیقه و '+d[1]+' ثانیه'
	elif len(d)==1:
		return d[0]+' ثانیه'
	else:
		return ':'.join(d)

def get_aparat_track_link(VId, quality):
	r=requests.get(f"https://www.aparat.com/video/video/embed/videohash/{VId}/vt/frame")
	page = r.content.decode('utf-8').split("var options = ")[1].split(" ;")[0]
	j=loads(page)
	for o in j['multiSRC'][-1]:
		if o['label']==quality: return o['src']
	return ''

def get_youtube_track_link(vid, quality, update):
	r=requests.get("https://youtubemultidownloader.org/scrapp/backend/yt-get.php?url=https://www.youtube.com/watch?v="+vid)
	j=r.json()
	for i in j['format']:
		if str(i['id'])==quality: return i['url']
	return ''

def extractYoutubePlaylist(pid, quality, update, bot):
	try:
		update.callback_query.edit_message_text("در حال پردازش، لطفا شکیبا باشید")
		respond=requests.get('https://www.youtube.com/playlist?list='+pid+'&hl=fa', cookies={'CONSENT':'YES+cb.20210328-17-p0.en+FX'})
		print(pid)
		j=loads(respond.content.decode('utf-8').split('var ytInitialData = ')[1].split(';</')[0])
		tracks=[]
		for i in parse('$..playlistVideoRenderer').find(j):
			tracks.append({'title': i.value['title']['accessibility']['accessibilityData']['label'], 'id': i.value['videoId']})
		data={'title': j['metadata']['playlistMetadataRenderer']['title'], 'description': j['metadata']['playlistMetadataRenderer']['description']}
		cn=parse('$..continuationCommand').find(j)
		if len(cn)>0:
			data['continuation']={'context': {'client': {'hl': 'fa', 'gl': 'US', 'clientName': 'WEB', 'clientVersion': '2.20220602.00.00', 'osName': 'Windows', 'osVersion': '10.0', 'platform': 'DESKTOP', 'clientFormFactor': 'UNKNOWN_FORM_FACTOR', 'timeZone': 'UTC', 'browserName': 'Chrome', 'browserVersion': '94.0.4430.70', 'utcOffsetMinutes': 0}, 'user': {'lockedSafetyMode': False}, 'request': {'useSsl': True}}, 'browseId': pid, 'continuation': cn[0].value['token']}
			data['nextPageUrl']='https://www.youtube.com/youtubei/v1/browse?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=false'
		p=playlist(tracks, data)
		update.callback_query.edit_message_text(f"عنوان: {p.title}\n{p.description}\nتعداد ترکها: {len(p.tracks)}")
		# time.sleep(5)
		links=[]
		for i in range(0, len(tracks)):
			update.callback_query.edit_message_text(f"در حال پردازش ترک {i+1} از {len(p.tracks)}...\n{p.tracks[i]['title']}")
			links.append(get_youtube_track_link(tracks[i]['id'], quality, update))
			if i==len(p.tracks)-1: p.next()
		f=open(f"{p.title}.txt", "w", encoding='utf-8')
		f.write('\n'.join(links))
		f.close()
		bot.send_document(chat_id=update.effective_chat.id, document=open(f"{p.title}.txt", "rb"), caption=f"لینک ترکهای پلیلیست {p.title}\nدارای {len(p.tracks)} ترک", reply_to_message_id=update.effective_message.reply_to_message.message_id)
		remove(f"{p.title}.txt")
		bot.delete_message(update.effective_chat.id, update.effective_message.message_id)
	except:
		traceback.print_exc()
		return False

def extractAparatPlaylist(pid, quality, update: Update, bot: Bot):
	try:
		update.callback_query.edit_message_text("در حال پردازش، لطفا شکیبا باشید")
		respond=requests.get("https://www.aparat.com/api/fa/v1/video/playlist/one/playlist_id/"+pid)
		tracks=[]
		j=respond.json()
		for i in parser.parse('$.included[?(@.type=="Video")].attributes').find(j):
			tracks.append({'title': i.value['title']+' - '+toTime(i.value['duration'])+' - '+i.value['date_exact'], 'id': i.value['uid']})
		data={'title': j['data']['attributes']['title'], 'description': j['data']['attributes']['description']}
		np=parse('$..list_videos_playlist.next_link').find(j)
		if len(np)>0:
			data['nextPageUrl']='https://aparat.com'+np[0].value
		p=playlist(tracks, data)
		update.callback_query.edit_message_text(f"عنوان: {p.title}\n{p.description}\nتعداد ترکها: {len(p.tracks)}")
		# time.sleep(5)
		links=[]
		for i in range(0, len(p.tracks)):
			update.callback_query.edit_message_text(f"در حال پردازش ترک {i+1} از {len(p.tracks)}...\n{p.tracks[i]['title']}")
			links.append(get_aparat_track_link(p.tracks[i]['id'], quality))
			if i==len(p.tracks)-1: p.next()
		f=open(f"{p.title}.txt", "w", encoding='utf-8')
		f.write('\n'.join(links))
		f.close()
		bot.send_document(chat_id=update.effective_chat.id, document=open(f"{p.title}.txt", "rb"), caption=f"لینک ترکهای پلیلیست {p.title}\nدارای {len(p.tracks)} ترک", reply_to_message_id=update.effective_message.reply_to_message.message_id)
		bot.delete_message(update.effective_chat.id, update.effective_message.message_id)
		remove(f"{p.title}.txt")
	except:
		traceback.print_exc()
		return False