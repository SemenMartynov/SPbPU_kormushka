from django.db import models
from django.utils import timezone

# Create your models here.

class Group(models.Model):
    title = models.CharField(max_length=200)
    about = models.CharField(max_length=500)
    def __str__(self):              # __unicode__ on Python 2
        return self.title

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    login = models.CharField(max_length=30)
    passwd = models.CharField(max_length=30)
    group = models.ForeignKey(Group)
    def __str__(self):              # __unicode__ on Python 2
        return self.first_name + self.last_name

class Post(models.Model):
		group = models.ForeignKey(Group)
		user = models.ForeignKey(User)
		text = models.CharField(max_length=500)
		amount = models.IntegerField(default=0)
		pub_date = models.DateTimeField('date published')
		def __str__(self):              # __unicode__ on Python 2
				return self.text
		def was_published_recently(self):
				return self.pub_date >= timezone.now() - datetime.timedelta(days=1)