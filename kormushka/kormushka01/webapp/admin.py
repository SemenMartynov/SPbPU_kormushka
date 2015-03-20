from django.contrib import admin
from webapp.models import Group, User, Post

# Register your models here

admin.site.register(Group)
admin.site.register(User)
admin.site.register(Post)