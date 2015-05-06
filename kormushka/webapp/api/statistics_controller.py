from django.shortcuts import render
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from webapp.models import Purchase
from loginsys.models import CustomUser
from django.contrib import auth
from django.db.models import Sum,Count
import json
import logging
from django.http import HttpResponse, Http404

#вывод страницы пользоватедя со списком покупок, в которых он участвует
@login_required(login_url="/login/")
def statistics(request):
	current_user_pk = auth.get_user(request).pk;
	
	UserСostsPaid = Purchase.objects.filter(user=current_user_pk, state=1).aggregate(sum=Sum('cost'))#атраты пользователя, которые оплачены
	if not UserСostsPaid['sum']: UserСostsPaid['sum'] = 0
	UserСostsNotPaid = Purchase.objects.filter(user=current_user_pk, state=0).aggregate(sum=Sum('cost'))#атраты пользователя, которые не оплачены
	if not UserСostsNotPaid['sum']: UserСostsNotPaid['sum'] = 0
	UserСostsAll = Purchase.objects.filter(user=current_user_pk).aggregate(sum=Sum('cost'))#Затраты пользователя за весь период
	if not UserСostsAll['sum']: UserСostsAll['sum'] = 0

	#Затраты на пользователя
	obj = Purchase.objects.annotate(amount=Count('pop__purchase')).filter(pop__user=current_user_pk)
	ForUserAll = 0
	for i in obj:
		ForUserAll = ForUserAll + i.cost/i.amount
	if not ForUserAll: ForUserAll = 0

	# #Затраты на отдел
	users = CustomUser.objects.filter(pop__depart=1).distinct()
	ForDepartAll = 0
	for user in users:
		obj = Purchase.objects.annotate(amount=Count('pop__purchase')).filter(pop__user=user.pk)
		for i in obj:
			ForDepartAll = ForDepartAll + i.cost/i.amount
	if not ForDepartAll: ForDepartAll = 0

	СostsPaid = Purchase.objects.filter(state=1).aggregate(sum=Sum('cost'))#Сумма оплаченные покупок
	if not СostsPaid['sum']: СostsPaid['sum'] = 0
	СostsNotPaid = Purchase.objects.filter(state=0).aggregate(sum=Sum('cost'))#Сумма неоплаченные покупок
	if not СostsNotPaid['sum']: СostsNotPaid['sum'] = 0
	СostsAll = Purchase.objects.aggregate(sum=Sum('cost'))#Сумма всех покупок
	if not СostsAll['sum']: СostsAll['sum'] = 0

	args={	'UserСostsPaid':UserСostsPaid['sum'], 'UserСostsAll':UserСostsAll['sum'], 'UserСostsNotPaid':UserСostsNotPaid['sum'],
			'ForUserAll':round(ForUserAll,2), 'ForDepartAll':round(ForDepartAll,2),
			'СostsNotPaid':СostsNotPaid['sum'], 'СostsPaid':СostsPaid['sum'], 'СostsAll':СostsAll['sum'],
			'title':'kormushka'}
	args.update(csrf(request))

	return render(request,'statistics/layout.html', args)

def usersStatistics(request):
	if request.is_ajax() and request.POST:
		return HttpResponse(json.dumps('true'))
	raise Http404