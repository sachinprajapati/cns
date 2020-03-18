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
	context = DataReport(dt)
	return render(request, "index.html", context)

def Reports(request):
	context = {}
	if request.method == 'POST':
		dt = datetime.strptime(request.POST.get("date"), "%Y-%m-%d")
		data = RatingReport(dt)
		return render(request, "reports.html", data)
	context["form"] = True
	return render(request, "reports.html", context)


def Summary(request):
	dt = timezone.localtime()
	if dt.hour < 8:
		dt = dt-timedelta(days=1)
	context = DataReport(dt)
	context.pop("data")
	return JsonResponse(context)


def getStatus(request):
	dt = timezone.localtime()
	if dt.hour < 8:
		dt = dt-timedelta(days=1)
	data = QueryDate(dt).order_by("-dt")
	d = data[:len(data)%10]
	if len(data)%10 == 0 and len(data) >= 10:
		d = data[:10]
	print("total count: ", len(data), len(d))
	last_data = json.loads(serializers.serialize("json", d))
	summary = DataReport(dt)
	if summary.get("data"):
		summary.pop("data")
	return JsonResponse({"data": [i['fields'] for i in last_data], "tcount": len(data)-len(d)+1, "summary": summary})

def ReportsMail(request):
	context = {}
	context["form"] = True
	if request.method == 'POST':
		dt = datetime.strptime(request.POST.get("date"), "%Y-%m-%d")
		report = RatingReport(dt)
		if report:
			report["dt"] = dt.date()
			msg_html = render_to_string('email.html', report)
			plain_message = strip_tags(msg_html)
			try:
				send_mail(
				'Daily Production Report',
				plain_message,
				'billgates@gmail.com',
				['gaganguptaj@gmail.com'],
				fail_silently=False,
				html_message=msg_html)
				context["form"] = False
			except Exception as e:
				context["errors"] = "Mail Not Sent, Please Check Internet Error"
				context["form"] = True	
		else:
			context["errors"] = "There is not Data on this Date {}".format(dt.date())
			context["form"] = True
	return render(request, "reportmail.html", context)