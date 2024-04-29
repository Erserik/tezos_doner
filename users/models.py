from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    # Add a field to store the contract.txt ID

    blockchain_contract_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    iin_number = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    blood_group = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(max_length=200, blank=True, null=True)
    # Add any additional fields or methods as needed

class Hospital(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

class HospitalManager(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)