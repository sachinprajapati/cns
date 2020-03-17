from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic.list import ListView
from django.utils import timezone
from datetime import datetime
from django.core import serializers
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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
	if context:
		data = context['data']
		context['tcount'] = len(data)
		context['data'] = data[len(data)-len(data)%10:]
		context['count'] = len(data)-len(context['data'])
		print(context)
	return render(request, "index.html", context)

def Reports(request):
	context = {}
	if request.method == 'POST':
		dt = datetime.strptime(request.POST.get("date"), "%Y-%m-%d").date()
		data = DataReport(dt)
		data["rating_data"] = Data.objects.filter(dt__day=dt.day, dt__month=dt.month, dt__year=dt.year).values("rating").annotate(count=Count('rating'))
		print(data["rating_data"])
		return render(request, "reports.html", data)
	context["form"] = True
	return render(request, "reports.html", context)

@csrf_exempt
def Procces(request):
	if request.POST == 'GET':
		data = request.GET
		f = Data._meta.get_all_field_names()
		print("data is ", f)
	return JsonResponse({"First": "sdf"})


def getStatus(request):
	dt = timezone.localtime()
	data = Data.objects.filter(dt__day=dt.day, dt__month=dt.month, dt__year=dt.year).order_by("-dt")
	d = data[:len(data)%10]
	if len(data)%10 == 0 and len(data) >= 10:
		d = data[:10]
	print("total count: ", len(data), len(d))
	last_data = json.loads(serializers.serialize("json", d))
	return JsonResponse({"data": [i['fields'] for i in last_data], "tcount": len(data)-len(d)+1})

def ReportsMail(request):
	context = {}
	context["form"] = True
	if request.method == 'POST':
		dt = datetime.strptime(request.POST.get("date"), "%Y-%m-%d").date()
		report = DataReport(dt)
		report["dt"] = dt
		msg_html = render_to_string('email.html', report)
		plain_message = strip_tags(msg_html)
		send_mail(
		    'Daily Production Report',
		    plain_message,
		    'billgates@gmail.com',
		    ['gaganguptaj@gmail.com'],
		    fail_silently=False,
		    html_message=msg_html
		)
		context["form"] = False	
	return render(request, "reportmail.html", context)