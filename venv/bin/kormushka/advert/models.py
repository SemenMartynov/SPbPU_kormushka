from django.db import models

# Create your models here.
class Advert(models.Model):
    class Meta:
        db_table = "advert"
    title = models.CharFiel(max_length = 200)
    text = models.TextField()
    date = models.DateTimeField()
    likes = model.Integeg()
