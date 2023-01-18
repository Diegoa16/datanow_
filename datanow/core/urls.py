from django.urls import path
from . import views
from core.dash_apps import realtime, history_, _forecast, _downloads

urlpatterns = [
    # Paths del core
    path('', views.home, name='home'),
    path('history', views.history, name='history'),
    path('forecast/', views.forecast, name='forecast'),
    path('downloads/', views.downloads, name='downloads'),
    path('alerts/', views.alerts, name='alerts'),
    path('sms/', views.sms, name='sms'),
    path('comparation/', views.comparation, name='comparation'),
]
