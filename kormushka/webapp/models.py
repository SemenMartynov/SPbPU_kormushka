from django.db import models
from loginsys.models import CustomUser

#Покупки
class Purchase(models.Model):
	name = models.CharField("Название",max_length=50)
	user = models.ForeignKey(CustomUser, verbose_name="Пользователь")
#	depart = models.ForeignKey(Depart,verbose_name = "Отдел")
	date = models.DateTimeField("Дата совершения",auto_now=True, blank=True)
	cost = models.FloatField("Сумма",default = 0)
	state = models.IntegerField("Состояние",default = 0)#оплачена или нет
	about = models.TextField(blank=True)
#	category = models.ForeignKey(Category)

	def __str__(self):
		return self.name