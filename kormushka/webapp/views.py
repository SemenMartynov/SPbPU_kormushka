from django.shortcuts import render, redirect
from django.contrib import auth
from django.core.context_processors import csrf

def index(request):

	return render(request,'index.html')