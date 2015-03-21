from django.contrib import admin
from advert.models import Advert, Comment

# Register your models here.
class AdvertInline(admin.StackedInline):
    model = Comment
    extra = 3

class AdvertAdmin(admin.ModelAdmin):
    fields = ['title', 'text', 'date']
    inlines = [AdvertInline]

admin.site.register(Advert, AdvertAdmin)
