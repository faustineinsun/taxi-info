from django.http import HttpResponse
from django_tables2   import RequestConfig
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from demo.models import Record, Account 
from demo.tables  import RecordTable
#from django.core.cache import cache
import os
import urlparse
import redis
import json

url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
r = redis.Redis(host=url.hostname, port=url.port, password=url.password)

# Create your views here.
#def login(request):
    #    return render(request, 'login.html')

@login_required(login_url="/") 
def logout_view(request): 
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/')
def tabularresults(request):
    table = RecordTable(Record.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'tabularresults.html', {"table": table})

@login_required(login_url="/") 
def graphicalsummary(request):
    return render(request, 'graphicalsummary.html')

@login_required(login_url="/") 
@api_view(['GET'])
def chartmorning(request):
    return Response(r.get("passengercount:morning"))

@login_required(login_url="/") 
@api_view(['GET'])
def chartafternoon(request):
    return Response(r.get("passengercount:afternoon"))

@login_required(login_url="/") 
@api_view(['GET'])
def chartevening(request):
    return Response(r.get("passengercount:evening"))

@login_required(login_url="/") 
@api_view(['GET'])
def chartnight(request):
    return Response(r.get("passengercount:night"))

@login_required(login_url="/") 
@api_view(['GET'])
def chartall(request):
    return Response(r.get("passengercount:all"))

@login_required(login_url="/") 
@api_view(['GET'])
def houronmap(request):
    h = request.GET['h']
    ary = [None]*3
    ary[0] = r.get("geojson:lines:"+str(h)) 
    ary[1] = r.get("geojson:startpoints:"+str(h)) 
    ary[2] = r.get("geojson:endpoints:"+str(h)) 
    return Response(ary)
