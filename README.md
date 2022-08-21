<h1>videoToLinkBot: A Telegram bot is written by Python and Django and Telegram bot library</h1>
<p>For my university project, I wrote a robot that receives telegram messages through Django (webhook) and responds to them.</p>
<h2>What can this bot do?</h2>
<p>Currently, if you send a playlist link from YouTube or Aparat site, it will extract the video link of that playlist and send those to you in a text file. (I used my personal experiences in this project and got help from some sites to get the video links.</p>
<p>Note: The bot language is Persian and can be accessed on Telegram with the username @v2link_bot</p>
<h2>How to run this bot on a server?</h2>
<p>To run this bot, you need a few things:</p>
<ul>
	<li>Python (usually 3.7 or higher)</li>
	<li>django version 3.2 or higher)</li>
	<li>python-telegram-bot version 13.13 (The version in which I wrote the bot)</li>
	<li><a href="https://pypi.org/project/jsonpath-ng/" target="blank">jsonpath_ng library</a></li>
</ul>
<p>After installing these items, you need to do a few things:</p>
<h3>1: Create a new django project:</h3>
<p>django-admin startproject v2link_bot</p>
<p>then extract this project content into your project directory, so the "bot" folder should be first folder in your directory, then v2link_bot and manage.py file.</p>
<h3>2: Set webhook:</h3>
<p>To receive updates from Telegram with Django, you need to set webhook. To know how to set it, refer to <a href="https://core.telegram.org/bots/webhooks" target="blank">Marvin's Marvellous Guide to All Things Webhook</a></p>
<h3>3: Install the bot app, configure it, and add it in created django project:</h3>
<p>By now you should have the bot folder in your django project folder. You need to set it up:</p>
<p>Go to the bot folder and edit the "views.py" file and put your bot token instead of YOUR_BOT_TOKEN in line 7.</p>
<p>Go to v2link_bot folder and open "settings.py" file and add bot to installed_apps:</p>
<pre>INSTALLED_APPS = [
    ...,
    'bot',
]
</pre>
<p>In the same folder, open the urls.py file and first, import the bot:</p>
<pre>from django.urls import path, include
from bot.views import callback
</pre>
<p>Next, redirect the bot path to the bot app:</p>
<pre>urlpatterns = [
    ...,
    path("bot", callback),
]</pre>
<p>Congratulations, you have completed the bot configuration.</p>
<h3>4: Configuring Django server to work with HTTPS</h3>
<p>The default Django manage.py runserver command doesn't support SSL; therefore, we need to use the alternative manage.py runserver_plus command, which is part of the Django Extensions package.</p>
<p>pip install django-extensions Werkzeug</p>
<p>open the settings.py file in your code editor and add django_extensions to the INSTALLED_APPS list:</p>
<pre>INSTALLED_APPS = [
    ...,
    'bot',
    'django_extensions'
]</pre>
<h2>starting the server:</h2>
<p>Use these commands to setting up the project:</p>
<p>python manage.py makemigrations<br>
python manage.py migrate</p>
<p>start the local development server in HTTPS mode by running the command:</p>
<p>python manage.py runserver_plus --cert-file cert.pem --key-file key.pem</p>
<p>Note: cert.pem and key.pem files are the files that you must have created in the set webhook guide.</p>
<p>Congratulations, the bot has run successfully! If there is a problem, be sure to raise it in the problems section.</p>
<h2>Additional explanations:</h2>
<p>This is my first project that I put on github. If there was a problem in the guide or a problem occurred in the program, etc., I would be happy if you report it.</p>
