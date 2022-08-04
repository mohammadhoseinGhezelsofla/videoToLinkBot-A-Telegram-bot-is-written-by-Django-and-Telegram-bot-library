from django.db import models

class User(models.Model):
	userId=models.BigIntegerField(primary_key=True, unique=True)
	firstname=models.CharField(max_length=64)
	lastname=models.CharField(max_length=64, null=True)

class Message(models.Model):
	messageId=models.BigIntegerField(primary_key=True, unique=True)
	messageText=models.TextField(max_length=4096)
	sender=models.ForeignKey(User, on_delete=models.CASCADE)

def getUser(userId):
	queries=User.objects.filter(userId__exact=userId)
	if queries.count()>0:
		return queries.get()
	else:
		return None

