from django.shortcuts import render, redirect
from django.contrib import auth
from django.core.context_processors import csrf

def login(request):
	args = {}
	args.update(csrf(request))
	if request.POST:
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		user = auth.authenticate(username=username,password=password)
		if user is not None:
			auth.login(request, user)
			return redirect('/')
		else:
			args['login_error'] = "Пользователь не найден"
			return render(request, 'login.html', args)
	else:
		return render(request,'login.html', args)

def logout(request):
	auth.logout(request)
	return redirect('/')