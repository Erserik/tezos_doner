from django.contrib import admin
from .models import CustomUser, Hospital, HospitalManager, Invitation, TimeSlot, Appointment

admin.site.register(CustomUser)
admin.site.register(Hospital)
admin.site.register(HospitalManager)
admin.site.register(Invitation)
admin.site.register(TimeSlot)
admin.site.register(Appointment)
