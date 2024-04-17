from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Add a field to store the contract ID

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
