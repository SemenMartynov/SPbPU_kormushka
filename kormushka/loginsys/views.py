from django.shortcuts import render, redirect
from django.contrib import auth
from django.core.context_processors import csrf

def login(request):
	return redirect('/')

def logout(request):
	return redirect('/')