from django.db import models
from data.constants import COMPANY_ID_MAX_LENGTH

# Create your models here.
""" 
id varchar(24 NOT NULL
company_name varchar(130) NULL
company_id varchar(24) NOT NULL
amount decimal(16,2) NOT NULL
status marchar(30) NOT NULL
created_at timestamp NOT NULL
updated_at timestamp NULL
"""
class Sales(models.Model):
  id = models.CharField(max_length=24, primary_key=True)
  company_name = models.CharField(max_length=130)
  company_id = models.CharField(max_length=COMPANY_ID_MAX_LENGTH)
  amount = models.DecimalField(max_digits=16, decimal_places=2)
  status = models.CharField(max_length=30)
  created_at = models.DateTimeField(editable=False, blank=False)
  updated_at = models.DateTimeField(editable=False, blank=False)


class Companies(models.Model):
    id = models.CharField(max_length=COMPANY_ID_MAX_LENGTH, primary_key=True)
    company_name = models.CharField(max_length=130)


class Charges(models.Model):
    id = models.CharField(max_length=24, primary_key=True)
    company = models.ForeignKey(Companies, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    status = models.CharField(max_length=30)
    created_at = models.DateTimeField(editable=False, blank=False)
    updated_at = models.DateTimeField(editable=False, blank=False)
