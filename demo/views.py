from django.http import HttpResponse
from demo.models import Record 
from demo.tables  import RecordTable
from django_tables2   import RequestConfig
from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request, 'login.html')

def tabularresults(request):
    table = RecordTable(Record.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'tabularresults.html', {"table": table})
