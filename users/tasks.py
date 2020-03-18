from __future__ import absolute_import

from celery import shared_task
from celery.task import periodic_task
from celery.task.schedules import crontab
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.utils import timezone
from users.views import *
from users.funcs import *

import time

@periodic_task(run_every=crontab(minute=32, hour=11))
# @periodic_task(run_every=timezone.timedelta(seconds=10))
def SendDataMail():
	print("sending mail")
	dt = timezone.localtime()
	report = RatingReport(dt)
	if report:
		report["dt"] = dt.date()
		msg_html = render_to_string('email.html', report)
		plain_message = strip_tags(msg_html)
		send_mail(
		'Daily Production Report',
		plain_message,
		'billgates@gmail.com',
		['gaganguptaj@gmail.com'],
		fail_silently=False,
		html_message=msg_html)


# @periodic_task(run_every=timezone.timedelta(seconds=3))
# def getData():
# 	data = Exact("RC 6.0HOLDV 83HOLDP1TRIPV151TRIPP1KNRP1HVP1OVER1HI  33.1TI  59.8HT 103TT  14CO1AC0$00")
# 	d = Data(**data)
# 	d.save()
# 	print("created data")