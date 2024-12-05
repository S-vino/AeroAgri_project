from django.db import models

# Create your models here.
class employee(models.Model):
    empid = models.CharField(max_length=20, unique=False, null=True)
    empname= models.CharField(max_length=200)
    empemail= models.EmailField(null=True,unique=True)
    empaddress = models.CharField(max_length=200)
    empphone=models.CharField(max_length=200)
    empdepartment = models.CharField(max_length=200)
    emppassword = models.PositiveBigIntegerField(null=True)
    grant = models.BooleanField(null=True, default=False)
    revoke = models.BooleanField(null=True, default=False)
    accept = models.BooleanField(null=True, default=False)
    decline = models.BooleanField(null=True, default=False)
    admit = models.BooleanField(null=True, default=False)
    deny = models.BooleanField(null=True, default=False)

