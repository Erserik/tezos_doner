from django.contrib import admin
from .models import *

admin.site.register(CustomUser)
admin.site.register(Hospital)
admin.site.register(HospitalManager)


