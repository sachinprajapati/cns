from django.urls import path
from users.views import *

app_name = 'users'

urlpatterns = [
    path('', Homepage, name="homepage"),
    path('reports/', Reports, name="reports"),
    path('report-mail/', ReportsMail, name="report-mail"),
    path('get-status/', getStatus, name="get-status")
]
