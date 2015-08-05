from django.http import HttpResponse
from demo.models import Record 
from demo.tables  import RecordTable
from django_tables2   import RequestConfig
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
#from django.core.cache import cache
import os
import urlparse
import redis
import json

url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
r = redis.Redis(host=url.hostname, port=url.port, password=url.password)

# Create your views here.
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

@api_view(['GET'])
def houronmap(request):
    h = request.GET['h']
    ary = [None]*3
    ary[0] = r.get("geojson:lines:"+str(h)) 
    ary[1] = r.get("geojson:startpoints:"+str(h)) 
    ary[2] = r.get("geojson:endpoints:"+str(h)) 
    return Response(ary)

