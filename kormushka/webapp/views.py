from django.shortcuts import render, redirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from webapp.models import Purchase,Depart,Category,PO
from webapp.forms import PurchaseForm
from loginsys.models import CustomUser
import datetime
import json
from rest_framework import viewsets
from webapp.serializers import CategorySerializer

@login_required(login_url="/login/")
def index(request):
	purchase = Purchase.objects.filter(user=request.user.pk)
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
	return redirect('/')
	
# ViewSets определяют способ отображения представлений.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer