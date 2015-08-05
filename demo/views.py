from django.http import HttpResponse
from demo.models import Record 
from demo.tables  import RecordTable
from django_tables2   import RequestConfig
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import redis
import os

# Create your views here.
redis_url = os.getenv('REDISTOGO_URL', 'redis://127.0.0.1:6379')
r = redis.from_url(redis_url)

def login(request):
    return render(request, 'login.html')

def tabularresults(request):
    table = RecordTable(Record.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'tabularresults.html', {"table": table})

def graphicalsummary(request):
    return render(request, 'graphicalsummary.html')

@api_view(['GET'])
def chartmorning(request):
    return Response(r.get("passengercount:morning"))

@api_view(['GET'])
def chartafternoon(request):
    return Response(r.get("passengercount:afternoon"))

@api_view(['GET'])
def chartevening(request):
    return Response(r.get("passengercount:evening"))

@api_view(['GET'])
def chartnight(request):
    return Response(r.get("passengercount:night"))

@api_view(['GET'])
def chartall(request):
    return Response(r.get("passengercount:all"))

