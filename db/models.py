import sys

try:
    from django.db import models
except Exception:
    print('Exception: Django Not Found, please install it with "pip install django".')
    sys.exit()


class Country(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10)

    def __str__(self):
        return self.name


# Sample User model
class User(models.Model):
    fullname = models.CharField(max_length=100, null=True)
    age = models.IntegerField(default=0, null=True)
    phone = models.CharField(max_length=20, null=True)
    level = models.CharField(max_length=30, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, related_name='user')

    chat_id = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=100, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Admin(models.Model):
    username = models.CharField(max_length=100, null=True)
    chat_id = models.CharField(max_length=100, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Message(models.Model):
    text = models.TextField(null=True)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)

    photo = models.CharField(max_length=300, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Reklama(models.Model):
    text = models.TextField(null=True)
    views_count = models.IntegerField(default=0, null=True)
    all_count = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.text


class ChannelMessage(models.Model):
    message_id = models.IntegerField(null=True)
    text = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
