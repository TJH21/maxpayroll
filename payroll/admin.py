from django.contrib import admin
from .models import  PayrollRun, Allowance, Deduction


admin.site.register(PayrollRun)
admin.site.register(Allowance)
admin.site.register(Deduction)