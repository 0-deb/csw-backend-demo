from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.contrib.postgres.fields import ArrayField


CAR_TYPE = (
    ("Petrol", "Petrol"),
    ("Diesel", "Diesel"),
    ("CNG", "CNG")
)

class Brands(models.Model):
	"""
	Brands of all vehicles
	"""
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=255, blank=False, unique=True, null=False)
	logo = models.CharField(max_length=500, blank=False, unique=False, null=False)

	def __str__(self):
		return f"<{self.id}> {self.name}"

	class Meta:
		db_table = 'Brands'
		verbose_name = 'Brand'
		managed = True


class Cars(models.Model):
	"""
	Cars of all brands
	"""
	id = models.BigAutoField(primary_key=True)
	brand = models.ForeignKey(to=Brands, on_delete=models.CASCADE)
	model = models.CharField(max_length=255,blank=False, null=False)
	image = models.CharField(max_length=500, blank=False, null=False)
	type = models.CharField(max_length=255, blank=False, null=False, choices=CAR_TYPE)

	def __str__(self):
		return f"<{self.brand.name}> {self.model}"

	class Meta:
		db_table = "Cars"
		verbose_name = 'Car'
		managed = True


class Orders(models.Model):
    """
    Order of Users
    """
    id = models.BigAutoField(primary_key=True)
    car = models.ForeignKey(to=Cars, on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    serviceList = models.JSONField(blank=False, null=False)
    email = models.CharField(max_length=255, blank=False, null=False, 
        validators=[
            RegexValidator(
                regex=r'[a-z0-9]{3,}\@[a-z0-9]{2,}\.[a-z]{2,}',
                message=r'Invalid email format'
            )
        ]
    )
    dateTime = models.DateTimeField(blank=False, null=False)