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

#@periodic_task(run_every=crontab(minute='*'))
@periodic_task(run_every=timezone.timedelta(seconds=10))
def SendDataMail():
	print("sending mail")
	# dt = timezone.localtime().date()
	# report = DataReport(dt)
	# report["dt"] = dt
	# msg_html = render_to_string('email.html', report)
	# send_mail(
	#     'Daily Production Report',
	#     msg_html,
	#     'billgates@gmail.com',
	#     ['gaganguptaj@gmail.com'],
	#     fail_silently=False,
	# )


@periodic_task(run_every=timezone.timedelta(seconds=3))
def getData():
	# while True:
	# 	print("getData")
	# 	time.sleep(1)
	data = Exact("RC 6.0HOLDV 83HOLDP1TRIPV151TRIPP1KNRP1HVP1OVER1HI  33.1TI  59.8HT 103TT  14CO1AC1$00")
	d = Data(**data)
	d.save()
	print("created data")