from django.shortcuts import render
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from webapp.models import Purchase,POP
from loginsys.models import CustomUser
from django.contrib import auth
from django.db.models import Sum,Count,Max,Min
from django.utils import timezone
from django.utils.timezone import utc
from django.http import HttpResponse, Http404
from dateutil.relativedelta import *
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

def getGraphYear(typeGraph,start_date, end_date,minDelta,pur):
	purchase = pur.get('purchase')
	sumOfYears = []
	labelsYears = []	
	step = relativedelta(years=1)
	firstStep = start_date.year
	lastStep = end_date.year +1

	for i in range (firstStep,lastStep):
		if i == lastStep:
			date_with_step = end_date
		else:
			date_with_step = start_date + step - minDelta

		#выдача данных по типу статистики
		if typeGraph == "custom":
			periodSumYear = purchase.filter(date__gte=start_date,date__lte=date_with_step).aggregate(sum=Sum('cost'))['sum']
		elif typeGraph == "userForAll":
			obj = purchase.filter(date__gte=start_date,date__lte=date_with_step)
			periodSumYear = 0
			for j in obj:
				periodSumYear = periodSumYear + j.cost/j.amount
		elif typeGraph == "departForAll":
			pop = pur.get('pop')
			obj = purchase.filter(date__gte=start_date,date__lte=date_with_step)
			periodSumYear = 0
			for i in obj:
				kol = pop.filter(purchase=i.pk).count()
				periodSumYear = periodSumYear + ((i.cost/i.amount)*kol*kol)
		labelsYears.append(i)
		if not periodSumYear: periodSumYear = 0
		sumOfYears.append(round(periodSumYear,2))
		start_date = start_date + step

	return 	{'label':labelsYears,'sum':sumOfYears} 

def getGraphMonth(typeGraph,start_date, end_date,minDelta,pur,deltaStep,lblShortMonth):
	purchase = pur.get('purchase')
	sumOfMonths = []
	labelsMonths = []

	step = relativedelta(months=1)													#шаг													
	sizePeriod = 12																	#период
	firstStep = start_date.month-1													# -1 , так как индекс идет с 0 
	lastStep = firstStep + (deltaStep.months + 1) + (deltaStep.years)*12           	#!!!Привязать к периоду
	if start_date.year != end_date.year:
		showShortMonth = True
	else:
		showShortMonth = False
	for i in range(firstStep,lastStep):
		if i == lastStep:
			date_with_step = end_date
		else:
			date_with_step = start_date + step - minDelta
		#выдача данных по типу статистики
		if typeGraph == "custom":
			periodSum = purchase.filter(date__gte=start_date,date__lte=date_with_step).aggregate(sum=Sum('cost'))['sum']
		elif typeGraph == "userForAll":
			obj = purchase.filter(date__gte=start_date,date__lte=date_with_step)
			periodSum = 0
			for j in obj:
				periodSum = periodSum + j.cost/j.amount
		elif typeGraph == "departForAll":
			pop = pur.get('pop')
			obj = purchase.filter(date__gte=start_date,date__lte=date_with_step)
			periodSum = 0
			for j in obj:
				kol = pop.filter(purchase=j.pk).count()
				periodSum = periodSum + ((j.cost/j.amount)*kol*kol)
		if showShortMonth:
			labelsMonths.append(lblShortMonth[i%sizePeriod] + "-" + str(start_date.year)[-2:])
		else:
			labelsMonths.append(lblShortMonth[i%sizePeriod])# + " " + str(start_date.year))
		logger = logging.getLogger(__name__)
		logger.error(showShortMonth)
		if not periodSum: periodSum = 0
		sumOfMonths.append(round(periodSum,2))
		start_date = start_date + step
	return {'label':labelsMonths,'sum':sumOfMonths}

def getGraphDay(typeGraph,start_date, end_date,minDelta,pur,allDelta,lblShortMonth):
	purchase = pur.get('purchase')
	sumOfDays = []
	labelsDays = []	
	step = relativedelta(days=1)
	for i in range (0,allDelta.days+1):
		date_with_step = start_date + step - minDelta
		if typeGraph == "custom":
			periodSum = purchase.filter(date__gte=start_date,date__lte=date_with_step).aggregate(sum=Sum('cost'))['sum']
		elif typeGraph == "userForAll":
			obj = purchase.filter(date__gte=start_date,date__lte=date_with_step)
			periodSum = 0
			for j in obj:
				periodSum = periodSum + j.cost/j.amount
		elif typeGraph == "departForAll":
			pop = pur.get('pop')
			obj = purchase.filter(date__gte=start_date,date__lte=date_with_step)
			periodSum = 0
			for i in obj:
				kol = pop.filter(purchase=i.pk).count()
				periodSum = periodSum + ((i.cost/i.amount)*kol*kol)
		labelsDays.append(str(start_date.day) + " " + lblShortMonth[start_date.month-1]) 
		if not periodSum: periodSum = 0
		sumOfDays.append(round(periodSum,2))
		start_date = start_date + step
	return {'label':labelsDays, 'sum':sumOfDays}

def getDetail(start_date,end_date,allDelta,deltaStep):
	#получение возможных вариантов детализации
	if allDelta.days <=32:
		detailByDays = True
	else:
		detailByDays = False

	if (allDelta.days <=32 and start_date.month != end_date.month) or (allDelta.days > 32 and deltaStep.years < 3):
		detailByMonths = True
	else:
		detailByMonths = False

	if (allDelta.days <=365 and start_date.year != end_date.year) or allDelta.days > 365:
		detailByYears = True
	else:
		detailByYears = False
	return {'detailByDays':detailByDays, 'detailByMonths':detailByMonths, 'detailByYears':detailByYears}

#данные для грфика
def graph(start_date,end_date,allDelta,deltaStep,purchase,typeDetailStat,typeGraph):
	minDelta = datetime.timedelta(microseconds=1)
	args = {}
	targetDetail = ""
	lblShortMonth = ["Янв","Фев","Мар","Апр","Май","Июн","Июл","Авг","Сен","Окт","Ноя","Дек"]
	if typeDetailStat != "first": detail = getDetail(start_date,end_date,allDelta,deltaStep)
	#получение выкладки

	if (allDelta.days >=730 and typeDetailStat == "first") or (typeDetailStat == "year" and detail.get('detailByYears')):
		sumAll = getGraphYear(typeGraph, start_date, end_date,minDelta,purchase)
		targetDetail = "detail-stat-year"
	elif (allDelta.days >32 and allDelta.days < 730 and typeDetailStat == "first") or (typeDetailStat == "month" and detail.get('detailByMonths')):
		sumAll = getGraphMonth(typeGraph, start_date, end_date,minDelta,purchase,deltaStep, lblShortMonth)
		targetDetail = "detail-stat-month"
	elif (allDelta.days <=32 and typeDetailStat == "first") or (typeDetailStat == "day" and detail.get('detailByDays')):
		sumAll = getGraphDay(typeGraph, start_date, end_date,minDelta,purchase,allDelta, lblShortMonth)
		targetDetail = "detail-stat-day"
	else:
		sumAll = {'label':[],'sum':[]}
	args.update({'sumOfPeriods': sumAll['sum'],'labels':sumAll['label'],'targetDetail':targetDetail})
	return args

def getDataForStat(request):
	if request.is_ajax() and request.POST:
		args = {}
		#получение начальной и конечной даты, а также набора покупок
		pur = Purchase.objects.all()
		date1 =  request.POST.get('date1')
		date2 =  request.POST.get('date2')
		typeStat = request.POST.get('typeStat')
		typeDetailStat  = request.POST.get('typeDetailStat')
		ForСostsAll = 0

		if not date1 or not date2: 
			minMaxDate = pur.aggregate(minDate=Min('date'),maxDate=Max('date'))

		if date1:
			date1 = date1.split("/")
			start_date = datetime.datetime(int(date1[2]), int(date1[1]), int(date1[0]),0,0,0).replace(tzinfo=utc)
			pur = pur.filter(date__gte=start_date)
		else:
			start_date = minMaxDate['minDate']
			start_date = start_date.replace(hour = 0, minute = 0, second =0, microsecond =0)
		if date2:
			date2 = date2.split("/")
			end_date = datetime.datetime(int(date2[2]), int(date2[1]), int(date2[0]),23,59,59).replace(tzinfo=utc)
			pur = pur.filter(date__lte=end_date)
		else:
			end_date = minMaxDate['maxDate']

		allDelta = end_date-start_date
		deltaStep = relativedelta(end_date, start_date.replace(day = 1))

		#выбор варианта статистики
		if typeStat == "personal-stat":
			UserType = request.POST.get('typeUser')
			if UserType == 'personal':
				current_user_pk = auth.get_user(request).pk
			elif UserType == 'users':
				current_user_pk = request.POST.get('userid')

			purСostsPaid = pur.filter(user=current_user_pk, state=1)					#затраты пользователя, которые оплачены
			purСostsNotPaid = pur.filter(user=current_user_pk, state=0)					#затраты пользователя, которые не оплачены
			purСostsAll = pur.filter(user=current_user_pk)
			typeGraph = "userForAll"

			#Затраты на пользователя
			obj = pur.annotate(amount=Count('pop__purchase')).filter(pop__user=current_user_pk)
			ForAllNumber = 0
			for i in obj:
				ForСostsAll = ForСostsAll + i.cost/i.amount
				ForAllNumber = ForAllNumber + 1
			if not ForСostsAll: ForСostsAll	 = 0

			resСostsForAll = graph(start_date,end_date,allDelta,deltaStep,{'purchase':obj},typeDetailStat,typeGraph)

			args.update({'sumOnСostsForAll':resСostsForAll.get('sumOfPeriods'),'labels':resСostsForAll.get('labels'),
						'ForСostsAll':round(ForСostsAll,2),'ForAllNumber':ForAllNumber})

		elif typeStat == "organization-stat":
			purСostsPaid = pur.filter(state=1)
			purСostsNotPaid = pur.filter(state=0)
			purСostsAll = pur
		elif typeStat == "depart-stat":
			departid =  request.POST.get('departid')
			purСostsPaid = pur.filter(depart=departid, state=1)
			purСostsNotPaid = pur.filter(depart=departid, state=0)
			purСostsAll = pur.filter(depart=departid)
			typeGraph = "departForAll"
			#Затраты на отдел
			obj = pur.annotate(amount=Count('pop__purchase')).filter(pop__depart=departid)
			pop = POP.objects.filter(depart=departid)
			for i in obj:
				kol = pop.filter(purchase=i.pk).count()
				ForСostsAll = ForСostsAll + ((i.cost/i.amount)*kol*kol)
			if not ForСostsAll: ForСostsAll = 0
			resСostsForAll = graph(start_date,end_date,allDelta,deltaStep,{'purchase':obj,'pop':pop},typeDetailStat,typeGraph)
			args.update({'sumOnСostsForAll':resСostsForAll.get('sumOfPeriods'),'labels':resСostsForAll.get('labels'),
						'ForСostsAll':round(ForСostsAll,2)})

		#общие рассчеты статистики
		typeGraph = "custom"
		СostsPaid = purСostsPaid.aggregate(sum=Sum('cost'),num=Count('id'))
		if not СostsPaid['sum']: СostsPaid['sum'] = 0
		resСostsPaid = graph(start_date,end_date,allDelta,deltaStep,{'purchase':purСostsPaid},typeDetailStat,typeGraph)

		СostsNotPaid = purСostsNotPaid.aggregate(sum=Sum('cost'),num=Count('id'))					
		if not СostsNotPaid['sum']: СostsNotPaid['sum'] = 0
		resСostsNotPaid = graph(start_date,end_date,allDelta,deltaStep,{'purchase':purСostsNotPaid},typeDetailStat,typeGraph)

		СostsAll = purСostsAll.aggregate(sum=Sum('cost'),num=Count('id'))		#затраты пользователя за весь период
		if not СostsAll['sum']: СostsAll['sum'] = 0
		resСostsAll = graph(start_date,end_date,allDelta,deltaStep,{'purchase':purСostsAll},typeDetailStat,typeGraph)

		if start_date > end_date:
			result = False
			args.update({'result':result})
		else:
			result = True
			args.update({'sumOnСostsPaid':resСostsPaid.get('sumOfPeriods'), 'labels':resСostsPaid.get('labels'),
						'sumOnСostsNotPaid':resСostsNotPaid.get('sumOfPeriods'), 'labels':resСostsNotPaid.get('labels'),
						'sumOnСostsAll':resСostsAll.get('sumOfPeriods'), 'labels':resСostsAll.get('labels'),
						'result':result})

		#возможность детализации на графике
		args.update(getDetail(start_date,end_date,allDelta,deltaStep))

		args.update({'СostsPaid':СostsPaid['sum'], 'СostsNotPaid':СostsNotPaid['sum'], 'СostsAll':СostsAll['sum'],
					'NumberPaid':СostsPaid['num'], 'NumberNotPaid':СostsNotPaid['num'], 'NumberAll':СostsAll['num'],
					'start_date':start_date.strftime("%d.%m.%Y"), 'end_date':end_date.strftime("%d.%m.%Y"), 'targetDetail':resСostsPaid.get('targetDetail')})

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