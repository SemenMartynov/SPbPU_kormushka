from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import ugettext_lazy as _

from loginsys.models import CustomUser

class CustomUserChangeForm(UserChangeForm):
    u"""Обеспечивает правильный функционал для поля с паролем и показ полей профиля."""
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    def clean_password(self):
        return self.initial["password"]

    class Meta:
        model = CustomUser
        fields = "__all__"

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm

    list_display = ('get_full_name', 'username', 'email', 'is_active', 'is_staff', 'is_superuser')

    fieldsets = (
    	(None, {'fields': ('username', 'password')}),
    	('Персональная информация',{'fields':('first_name', 'last_name', 'email', 'image')}),
    	('Права доступа',{'fields':('is_active', 'is_staff', 'is_superuser')})
    	)

admin.site.unregister(User)
admin.site.register(CustomUser, CustomUserAdmin)