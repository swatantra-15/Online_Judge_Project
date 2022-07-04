from django.contrib import admin

# Register your models here.
from .models import Problems,Test_Case,Solutions
admin.site.register(Problems)
admin.site.register(Test_Case)