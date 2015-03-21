from django.db import models

# Create your models here.
class Advert(models.Model):
    class Meta():
        db_table = 'adverts'
    title = models.CharField(max_length = 200)
    text = models.TextField()
    date = models.DateTimeField()
    like = models.IntegerField(default=0)

class Comment(models.Model):
    class Meta():
        db_table = 'comments'
    text = models.TextField()
    advert = models.ForeignKey(Advert)

