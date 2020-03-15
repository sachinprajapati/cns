from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic.list import ListView
from django.utils import timezone
from datetime import datetime
from django.core import serializers

from users.models import Data
from users.funcs import *

import json
import minimalmodbus

def Homepage(request):
	try:
		instrument = minimalmodbus.Instrument('/dev/ttyUSB1', 1) 
	except Exception as e:
		context = {
			"errors": "No Communication",
		}
	dt = timezone.localtime()
	context = DataReport(dt.date())
	data = context['data']
	print("total count: ", len(data))
	context['tcount'] = len(data)
	context['data'] = data[:len(data)%10]
	context['count'] = len(data)-len(context['data'])
	context['content'] = DataReport(dt.date())
	return render(request, "index.html", context)

def Reports(request):
	context = {}
	if request.method == 'POST':
		dt = datetime.strptime(request.POST.get("date"), "%Y-%m-%d").date()
		data = DataReport(dt)
		return render(request, "reports.html", data)
	context["form"] = True
	return render(request, "reports.html", context)


def Procces(request):
	Data.objects.create(hold_v=True, trip_v=True)
	return JsonResponse({"First": True})


def getStatus(request):
	dt = timezone.localtime()
	data = Data.objects.filter(dt__day=dt.day, dt__month=dt.month, dt__year=dt.year).order_by("-dt")
	print("total count: ", len(data))
	d = data[:len(data)%10]
	data = json.loads(serializers.serialize("json", d, fields=('dt','hold')))
	return JsonResponse({"data": [i['fields'] for i in data]})