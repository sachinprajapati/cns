from django.urls import path
from users.views import *

app_name = 'users'

urlpatterns = [
    path('', Homepage, name="homepage"),
    path('reports/', Reports, name="reports"),
    path('procces/', Procces, name="procces"),
    path('get-status/', getStatus, name="get-status")
]
