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

from users.models import *
from users.funcs import *

import json

def Homepage(request):
	dt = timezone.localtime()
	context = DataReport(dt)
	return render(request, "index.html", context)

def Reports(request):
	context = {}
	if request.method == 'POST':
		tm = request.POST.get("time")
		etm = request.POST.get("etime")
		edt = request.POST.get("edate")
		if tm: 
			dt = datetime.strptime(request.POST.get("date")+" "+tm, "%Y-%m-%d %H:%M")
		else:
			dt = datetime.strptime(request.POST.get("date"), "%Y-%m-%d")
		if etm and edt: 
			edt = datetime.strptime(edt+" "+etm, "%Y-%m-%d %H:%M")
		elif edt:
			edt = datetime.strptime(edt, "%Y-%m-%d")
		elif etm:
			edt = datetime.strptime(request.POST.get("date")+" "+etm, "%Y-%m-%d %H:%M")
		print("dt is", dt, "end time",edt)
		data = RatingReport(dt, edt)
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
	d = data[:len(data)%15]
	if len(data)%15 == 0 and len(data) >= 15:
		d = data[:15]
	last_data = json.loads(serializers.serialize("json", d))
	summary = DataReport(dt)
	if summary.get("data"):
		summary.pop("data")
	return JsonResponse({"data": [i['fields'] for i in last_data], "tcount": len(data)-len(d)+1, "summary": summary})

def ReportsMail(request):
	context = {}
	context["form"] = True
	if request.method == 'POST':
		tm = request.POST.get("time")
		etm = request.POST.get("etime")
		edt = request.POST.get("edate")
		if tm: 
			dt = datetime.strptime(request.POST.get("date")+" "+tm, "%Y-%m-%d %H:%M")
		else:
			dt = datetime.strptime(request.POST.get("date"), "%Y-%m-%d")
		if etm and edt: 
			edt = datetime.strptime(edt+" "+etm, "%Y-%m-%d %H:%M")
		elif edt:
			edt = datetime.strptime(edt, "%Y-%m-%d")
		elif etm:
			edt = datetime.strptime(request.POST.get("date")+" "+etm, "%Y-%m-%d %H:%M")
		report = RatingReport(dt, edt)
		emails = [e.email_id for e in Email.objects.all()]
		if report and emails:
			report["dt"] = dt
			report["edt"] = edt
			msg_html = render_to_string('email.html', report)
			plain_message = strip_tags(msg_html)
			try:
				send_mail('Daily Production Report', plain_message,'cnsharidwar@gmail.com', emails,
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