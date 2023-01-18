from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'core/home.html')

def history(request):
    return render(request, 'core/history.html')

def forecast(request):
    return render(request, 'core/forecast.html')

def downloads(request):
    return render(request, 'core/downloads.html')

def alerts(request):
    return render(request, 'core/alerts.html')
    
def comparation(request):
    return render(request, 'core/comparation.html')

def sms(request):
    return render(request, 'core/sms.html')
    
