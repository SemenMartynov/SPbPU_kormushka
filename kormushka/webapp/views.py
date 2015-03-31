from django.shortcuts import render, redirect
from django.contrib import auth
from django.core.context_processors import csrf

def index(request):

	return render(request,'list.html', {
		'title':'kormushka',
		'user':auth.get_user(request),
	})