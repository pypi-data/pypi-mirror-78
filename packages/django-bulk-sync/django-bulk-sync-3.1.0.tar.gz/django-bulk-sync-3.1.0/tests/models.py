from django.conf import settings
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=140)


class Employee(models.Model):
    age = models.IntegerField()
    name = models.CharField(max_length=140, blank=True, null=True)

    company = models.ForeignKey(Company, models.CASCADE)

    def __str__(self):
        return "Employee: {} age {} company {}".format(self.name, self.age, self.company_id)
