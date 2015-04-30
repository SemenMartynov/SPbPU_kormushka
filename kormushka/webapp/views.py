from django.shortcuts import render, redirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from webapp.models import Purchase,Depart,Category,PO,POP
from webapp.forms import PurchaseForm
from loginsys.models import CustomUser
from django.http import HttpResponse
import datetime
import json
import logging
from webapp.serializers import AllFieldsSerializer

@login_required(login_url="/login/")
def index(request):
	k=[]
	l = POP.objects.filter(user=request.user.pk)
	for i in l:
	 	k.append(i.purchase.id)

	purchase = Purchase.objects.filter(pk__in=k)
	depart = PO.objects.filter(user=request.user.pk)
	category = Category.objects.all()
	args = {'purchase' : purchase,'title':'kormushka','user':auth.get_user(request),'category':category,'depart':depart, 'formadd':'collapse'}# formadd - форма добавления свернута
	args.update(csrf(request))
	return render(request,'list.html', args)

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

				lastPurchase =  Purchase.objects.latest('id').pk
				userpk = request.POST['userpk'].split(",")
				userpk = list(set(userpk))
				for i in userpk:
					party = POP(user=CustomUser.objects.get(id=i), purchase=Purchase.objects.get(id=lastPurchase), depart=Depart.objects.get(id=1))
					party.save()

	return redirect('/')

def getUsersByName(request):
	name = request.POST.get('name')
	ser = AllFieldsSerializer()

	all_objects = list(CustomUser.objects.filter(last_name__icontains=name))
	l = list()
	for obj in all_objects:
		l.append({"label": obj.get_full_name(), "value": obj.pk})
	return HttpResponse(json.dumps(l))

def getPurchaseUsers(request):
	purchaseId = request.POST.get('purchaseId')

	l = POP.objects.filter(purchase=Purchase.objects.get(id=purchaseId))
	k=[]
	for i in l:
	 	k.append(i.user.id)
	logger = logging.getLogger(__name__)
	logger.warn(k)
	user = list(CustomUser.objects.filter(pk__in=k))
	li=list()
	for obj in user:
		li.append({"label": obj.get_full_name(), "pk": obj.pk})
	return HttpResponse(json.dumps(li))		