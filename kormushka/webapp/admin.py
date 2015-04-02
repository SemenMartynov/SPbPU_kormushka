from django.contrib import admin
from webapp import models

admin.site.register(models.Purchase)
admin.site.register(models.Category)
admin.site.register(models.Depart)
admin.site.register(models.POP)
admin.site.register(models.PO)