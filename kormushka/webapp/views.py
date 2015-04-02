from django.shortcuts import render, redirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from webapp.models import Purchase,Depart,Category,PO
from webapp.forms import PurchaseForm
from loginsys.models import CustomUser
import datetime

@login_required(login_url="/login/")
def index(request):
	purchase = Purchase.objects.filter(user=request.user.pk)
	depart = PO.objects.filter(user=request.user.pk)
	category = Category.objects.all()
	args = {'purchase' : purchase,'title':'kormushka','user':auth.get_user(request),'category':category,'depart':depart}
	args.update(csrf(request))
	return render(request,'list.html', args)

@login_required(login_url="/login/")
def addpurchase(request):
	if request.POST:
		form = PurchaseForm(request.POST, request.FILES)
		if form.is_valid():
			purchase = form.save(commit=False)
			purchase.user = CustomUser.objects.get(id=auth.get_user(request).pk)
			purchase.date = datetime.datetime.now()
			purchase.state = 0
			form.save()
	return redirect('/')