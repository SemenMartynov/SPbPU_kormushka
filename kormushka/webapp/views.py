from django.shortcuts import render, redirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from webapp.models import Purchase
from webapp.forms import PurchaseForm
from loginsys.models import CustomUser
import datetime

@login_required(login_url="/login/")
def index(request):
	purchase = Purchase.objects.filter(user=request.user.pk)
	args = {'purchase' : purchase,'title':'kormushka','user':auth.get_user(request)}
	args.update(csrf(request))
	return render(request,'list.html', args)

