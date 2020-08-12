from __future__ import absolute_import

from celery import shared_task
from celery.task import periodic_task
from celery.task.schedules import crontab
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.utils import timezone
from datetime import datetime, timedelta

from users.views import *
from users.funcs import *

from .models import *

import time

@periodic_task(run_every=crontab(minute=0, hour='8,9,10,11,12,21,22'))
#@periodic_task(run_every=timezone.timedelta(seconds=10))
def SendDataMail():
	print("sending mail")
	dt = timezone.localtime()
	report = RatingReport(dt - timedelta(days=1))
	to_send = MailStatus.objects.filter(dt__day=dt.day, dt__month=dt.month, dt__year=dt.year)
	emails = [e.email_id for e in Email.objects.all()]
	if report and emails and not to_send:
		report["dt"] = dt
		msg_html = render_to_string('email.html', report)
		plain_message = strip_tags(msg_html)
		if send_mail(
			'Daily Production Report',
			plain_message,
			'cnsharidwar@gmail.com',
			emails,
			fail_silently=False,
			html_message=msg_html):
			m = MailStatus.objects.create()
			m.save()
			print("mail sent")



# @periodic_task(run_every=timezone.timedelta(seconds=3))
# def getData():
# 	data = Exact("RC 6.0HOLDV 83HOLDP1TRIPV151TRIPP1KNRP1HVP1OVER1HI  33.1TI  59.8HT 103TT  14CO1AC0$00")
# 	d = Data(**data)
# 	d.save()
# 	print("created data")