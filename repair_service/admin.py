from django.contrib import admin

from .models import *

admin.site.register(Sales_Order)
admin.site.register(Work_Order)
admin.site.register(Repair)
admin.site.register(CustomerContact)
admin.site.register(CustomerAddress)
admin.site.register(Expenditure_Item)
admin.site.register(Revenue_Item)
