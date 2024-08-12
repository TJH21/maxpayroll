from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    established_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


def get_default_company():
    default_company = Company.objects.first()
    if default_company:
        return default_company.id
    else:
        return None  # Allow None if no company exists

class Department(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='departments', null=True, blank=True, default=get_default_company)

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    dob = models.DateField(null=True, blank=True)
    tax_code = models.CharField(max_length=10)
    ni_number = models.CharField(max_length=10)
    utr_number = models.CharField(max_length=10)
    paye_reference_number = models.CharField(max_length=100, unique=True)
    paye_office = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
