from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .botApi import botApi
from telegram import Update
from json import loads

botInstance=botApi("YOUR_BOT_TOKEN")

@csrf_exempt
def callback(request):
	global botInstance
	if request.method=="POST":
		botInstance.handle(Update.de_list(loads("["+request.body.decode("utf-8")+"]"), botInstance))
		return HttpResponse("ok")
	else:
		return HttpResponse("it is get, not post!")
