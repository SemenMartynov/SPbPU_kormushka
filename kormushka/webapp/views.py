from django.shortcuts import render, redirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from webapp.models import Purchase,Depart,Category,PO,POP
from webapp.forms import PurchaseForm
from loginsys.models import CustomUser
from django.http import HttpResponse
from webapp.ldap_sync import LdapSynchronizer
from django.db.models import Q
import datetime
import json
import logging

#вывод страницы пользоватедя со списком покупок, в которых он участвует
@login_required(login_url="/login/")
def index(request):
	purchase = Purchase.objects.filter(pop__user=request.user.pk)# список покупок, в которых участвует пользователь
	depart = PO.objects.filter(user=request.user.pk)
	category = Category.objects.all()
	args = {'purchase' : purchase,'title':'kormushka','user':auth.get_user(request),'category':category,'depart':depart, 'formadd':'collapse'}# formadd - форма добавления свернута
	args.update(csrf(request))
	return render(request,'profile/layout.html', args)

#добавление покупки
@login_required(login_url="/login/")
def addpurchase(request):
	args = {}
	args.update(csrf(request))
	if request.POST:
		form = PurchaseForm(request.POST, request.FILES)
		if form.is_valid():
			#проверяем, состоит ли пользователь в указанной группе. Защищает от подмены value.
			po = PO.objects.filter(user = request.user.pk, depart = request.POST['depart']) 
			if po:
				purchase = form.save(commit=False)
				purchase.user = CustomUser.objects.get(id=auth.get_user(request).pk)
				purchase.date = datetime.datetime.now()
				purchase.state = 0
				form.save()

				#Добавление записей в POP
				lastPurchase =  Purchase.objects.latest('id').pk	#получаем id только что добавленной покупки
				userpk = request.POST['userpk'].split(",")			#получаем список пользователей
				departpk = request.POST['departpk'].split(",")		#получаем список отделов, в которых состоят пользователи
				UserInDepart=dict(zip(userpk,departpk))				#выставляем соответствие: "пользователь" - "группа"
				UserInDepart[str(auth.get_user(request).pk)] = request.POST['depart'] #добавляем самого пользователя в покупку
				KeysUser = list(UserInDepart.keys())				#получаем список ключей - пользователей, участвующих в покупке
				for key in KeysUser:
					if key!='' and UserInDepart[key]!='':				#Если ключ или значения не путые
						if PO.objects.filter(user=key,depart=UserInDepart[key]):	#Если такой пользователь есть в базе
							party = POP(user=CustomUser.objects.get(id=key), purchase=Purchase.objects.get(id=lastPurchase), depart=Depart.objects.get(id=UserInDepart[key]))
							party.save()

	return redirect('/')

#получение списка пользователей для добавлении в покупку
def getUsersByName(request):	
	name = request.POST.get('name')

	all_objects = list(PO.objects.filter(Q(user__last_name__icontains=name) | Q(user__first_name__icontains=name) | Q(depart__name__icontains=name)))
	UserInDepart = list()
	for obj in all_objects:
		UserInDepart.append({"label": obj.user.get_full_name() + ' (' + obj.depart.name + ')', "userid": obj.user.pk, "departid": obj.depart.pk})
	return HttpResponse(json.dumps(UserInDepart))

#получения списка пользователей, участвующих в совершенной покупке
def getPurchaseUsers(request):
	purchaseId = request.POST.get('purchaseId')
	if POP.objects.filter(user=auth.get_user(request).pk,purchase=purchaseId):
		pop = POP.objects.filter(purchase=purchaseId)# список пользователей, которые участвуют в покупке
		UserInPurchase=list()
		for obj in pop:
			UserInPurchase.append({"label": obj.user.get_full_name(), "pk": obj.user.pk, "depart": obj.depart.name})
		return HttpResponse(json.dumps(UserInPurchase))
	return HttpResponse(json.dumps("error"))

def ldapSync(request):

    sync = LdapSynchronizer()
    result = sync.sync()

    return HttpResponse(json.dumps({"result": result}))
