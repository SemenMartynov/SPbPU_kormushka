from django.shortcuts import render
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib import auth
import json
from django.http import HttpResponse, Http404

#вывод страницы пользоватедя со списком покупок, в которых он участвует
@login_required(login_url="/login/")
def statistics(request):
	args={}
	args.update(csrf(request))
	return render(request,'statistics/layout.html', args)