from django.shortcuts import render
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from webapp.models import Purchase
from loginsys.models import CustomUser
from django.contrib import auth
from django.db.models import Sum,Count,Max,Min
from django.utils import timezone
from django.utils.timezone import utc
from django.http import HttpResponse, Http404
import json
import logging
import datetime

#вывод страницы пользоватедя со списком покупок, в которых он участвует
@login_required(login_url="/login/")
def statistics(request):
	current_user_pk = auth.get_user(request).pk;
	# date1 = date2 - datetime.timedelta(days=30)
	args={'title':'kormushka'}
	args.update(csrf(request))
	return render(request,'statistics/layout.html', args)

def personalStatistics(request):
	if request.is_ajax() and request.POST:
		UserType = request.POST.get('type')
		if UserType == 'personal':
			current_user_pk = auth.get_user(request).pk
		elif UserType == 'users':
			current_user_pk = request.POST.get('userid')

		date1 =  request.POST.get('date1')
		date2 =  request.POST.get('date2')
		pur = Purchase.objects.all()
		if date1:
			date1 = date1.split("/")
			start_date = datetime.datetime(int(date1[2]), int(date1[1]), int(date1[0]),0,0,0).replace(tzinfo=utc)
			pur = pur.filter(date__gte=start_date)
		if date2:
			date2 = date2.split("/")
			end_date = datetime.datetime(int(date2[2]), int(date2[1]), int(date2[0]),23,59,59).replace(tzinfo=utc)
			pur = pur.filter(date__lte=end_date)

		UserСostsPaid = pur.filter(user=current_user_pk, state=1).aggregate(sum=Sum('cost'),num=Count('id'))#атраты пользователя, которые оплачены
		if not UserСostsPaid['sum']: UserСostsPaid['sum'] = 0
		UserСostsNotPaid = pur.filter(user=current_user_pk, state=0).aggregate(sum=Sum('cost'),num=Count('id'))#атраты пользователя, которые не оплачены
		if not UserСostsNotPaid['sum']: UserСostsNotPaid['sum'] = 0
		UserСostsAll = pur.filter(user=current_user_pk).aggregate(sum=Sum('cost'),num=Count('id'))#Затраты пользователя за весь период
		if not UserСostsAll['sum']: UserСostsAll['sum'] = 0

		#Затраты на пользователя
		obj = pur.annotate(amount=Count('pop__purchase')).filter(pop__user=current_user_pk)
		ForUserСostsAll = 0
		ForUserAllNumber = 0
		for i in obj:
			ForUserСostsAll = ForUserСostsAll + i.cost/i.amount
			ForUserAllNumber = ForUserAllNumber + 1
		if not ForUserСostsAll: ForUserСostsAll	 = 0
		args={	'UserСostsPaid':UserСostsPaid['sum'], 'UserСostsNotPaid':UserСostsNotPaid['sum'], 'UserСostsAll':UserСostsAll['sum'], 'ForUserСostsAll':round(ForUserСostsAll,2),
				'UserNumberPaid':UserСostsPaid['num'], 'UserNumberNotPaid':UserСostsNotPaid['num'], 'UserNumberAll':UserСostsAll['num'], 'ForUserAllNumber':ForUserAllNumber}		
		return HttpResponse(json.dumps(args))
	raise Http404

def departsStatistics(request):
	if request.is_ajax() and request.POST:
		departid =  request.POST.get('departid')
		date1 =  request.POST.get('date1')
		date2 =  request.POST.get('date2')
		pur = Purchase.objects.all()
		if date1:
			date1 = date1.split("/")
			start_date = datetime.datetime(int(date1[2]), int(date1[1]), int(date1[0]),0,0,0).replace(tzinfo=utc)
			pur = pur.filter(date__gte=start_date)
		if date2:
			date2 = date2.split("/")
			end_date = datetime.datetime(int(date2[2]), int(date2[1]), int(date2[0]),23,59,59).replace(tzinfo=utc)
			pur = pur.filter(date__lte=end_date)


		
		DepartСostsPaid = pur.filter(depart=departid, state=1).aggregate(sum=Sum('cost'),num=Count('id'))#Затраты отдела оплаченные
		if not DepartСostsPaid['sum']: DepartСostsPaid['sum'] = 0
		DepartСostsNotPaid = pur.filter(depart=departid, state=0).aggregate(sum=Sum('cost'),num=Count('id'))#Затраты отдела неоплаченные
		if not DepartСostsNotPaid['sum']: DepartСostsNotPaid['sum'] = 0
		DepartСostsAll = pur.filter(depart=departid).aggregate(sum=Sum('cost'),num=Count('id'))#Затраты отдела всего
		if not DepartСostsAll['sum']: DepartСostsAll['sum'] = 0

		#Затраты на отдел
		users = CustomUser.objects.filter(pop__depart=departid).distinct()
		ForDepartAll = 0
		for user in users:
			obj = pur.annotate(amount=Count('pop__purchase')).filter(pop__user=user.pk,pop__depart=departid)
			for i in obj:
				ForDepartAll = ForDepartAll + i.cost/i.amount
		if not ForDepartAll: ForDepartAll = 0
		args={	'DepartСostsPaid':DepartСostsPaid['sum'], 'DepartСostsNotPaid': DepartСostsNotPaid['sum'], 'DepartСostsAll': DepartСostsAll['sum'], 'ForDepartAll':round(ForDepartAll,2),
				'DepartNumberPaid':DepartСostsPaid['num'], 'DepartNumberNotPaid': DepartСostsNotPaid['num'], 'DepartNumberAll': DepartСostsAll['num']}
		return HttpResponse(json.dumps(args))
	raise Http404

def organizationStatistics(request):
	if request.is_ajax() and request.POST:

		pur = Purchase.objects.all()
		date1 =  request.POST.get('date1')
		date2 =  request.POST.get('date2')
		if date1:
			date1 = date1.split("/")
			start_date = datetime.datetime(int(date1[2]), int(date1[1]), int(date1[0]),0,0,0).replace(tzinfo=utc)
			pur = pur.filter(date__gte=start_date)
		if date2:
			date2 = date2.split("/")
			end_date = datetime.datetime(int(date2[2]), int(date2[1]), int(date2[0]),23,59,59).replace(tzinfo=utc)
			pur = pur.filter(date__lte=end_date)

		СostsPaid = pur.filter(state=1).aggregate(sum=Sum('cost'),num=Count('id'))#Сумма оплаченные покупок
		if not СostsPaid['sum']: СostsPaid['sum'] = 0
		СostsNotPaid = pur.filter(state=0).aggregate(sum=Sum('cost'),num=Count('id'))#Сумма неоплаченные покупок
		if not СostsNotPaid['sum']: СostsNotPaid['sum'] = 0
		СostsAll = pur.aggregate(sum=Sum('cost'),num=Count('id'))#Сумма всех покупок
		if not СostsAll['sum']: СostsAll['sum'] = 0

		args={	'СostsNotPaid':СostsNotPaid['sum'], 'СostsPaid':СostsPaid['sum'], 'СostsAll':СostsAll['sum'],
				'NumberNotPaid':СostsNotPaid['num'], 'NumberPaid':СostsPaid['num'], 'NumberAll':СostsAll['num']}
		return HttpResponse(json.dumps(args))
	raise Http404

def getDateForPeriod(request):
	if request.is_ajax() and request.POST:
		periodType =  request.POST.get('type')
		date2 = datetime.datetime.now().date()
		if periodType=='day': date1=date2
		elif periodType=='week': date1 = date2 - datetime.timedelta(days=6)
		elif periodType=='month': date1 = date2 - datetime.timedelta(days=29)
		elif periodType=='year': date1 = date2 - datetime.timedelta(days=364)
		else: date1 =  datetime.datetime.now().date()
		args={'date1':date1.strftime("%d/%m/%Y"), 'date2':date2.strftime("%d/%m/%Y")}
		return HttpResponse(json.dumps(args))
	raise Http404