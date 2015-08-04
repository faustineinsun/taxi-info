import django_tables2 as tables
from demo.models import Record 

class RecordTable(tables.Table):
    class Meta:
        model = Record
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
