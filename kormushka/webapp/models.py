from django.db import models
from loginsys.models import CustomUser

#Тип покупки
class Category(models.Model):
	name = models.CharField("Тип покупки", max_length = 30)

	def __str__(self):
		return self.name

#Отделы
class Depart(models.Model):
	name = models.CharField("Название",max_length=100)
	depart = models.IntegerField("Состоит в",default = 0)

	def __str__(self):
		return self.name

#Покупки
class Purchase(models.Model):
	name = models.CharField("Название",max_length=50)
	user = models.ForeignKey(CustomUser, verbose_name="Пользователь")
	depart = models.ForeignKey(Depart,verbose_name = "Отдел")
	date = models.DateTimeField("Дата совершения",auto_now=True, blank=True)
	cost = models.IntegerField("Сумма",default = 0)
	state = models.IntegerField("Состояние",default = 0)#оплачена или нет 0-не оплачено, 1-оплачено
	about = models.TextField(blank=True)
	category = models.ForeignKey(Category)

	def __str__(self):
		return self.name

#ПОП - Покупатель - Отдел - Покупка
class POP(models.Model):
	user = models.ForeignKey(CustomUser, verbose_name="Пользователь")
	depart = models.ForeignKey(Depart, verbose_name = "Отдел")
	purchase = models.ForeignKey(Purchase, verbose_name = "Покупка")

	def __str__(self):
		return '%s %s (%s) - %s' % (self.user.last_name, self.user.first_name, self.depart.name,self.purchase.name)

#ПО - Покупатель - Отдел
class PO(models.Model):
	user = models.ForeignKey(CustomUser, verbose_name = "Пользователь")
	depart = models.ForeignKey(Depart, verbose_name = "Отдел")

	def __str__(self):
		return '%s %s (%s)' % (self.user.last_name, self.user.first_name, self.depart.name)