from django.contrib import admin
from advert.models import Advert, Comment

# Register your models here.
class AdvertAdmin(admin.ModelAdmin):
    fields = ['title', 'text', 'date']

admin.site.register(Advert, AdvertAdmin)
