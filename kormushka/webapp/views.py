from django.shortcuts import render, redirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login/")
def index(request):

	return render(request,'list.html', {
		'title':'kormushka',
		'user':auth.get_user(request),
	})