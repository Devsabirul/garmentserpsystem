from django.contrib import admin
from .models import *
admin.site.register([Employees,Atandents])
admin.site.register([Products,Companies,ProductDelivery])
admin.site.register([Invoice,InvoiceItem])
