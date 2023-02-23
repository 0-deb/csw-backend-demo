from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, validate_ipv46_address
from rest_framework.fields import ListField

import re


REGEX_DOMAIN = r'^([0-9a-z]{1,20}((\-|){1,18}[0-9a-z]{1,20}){1,31}\.){1,4}[0-9a-z]{1,61}$'

def validateURL(value):
	validate = URLValidator(schemes=["http", "https"])
	try:
		validate(value)

	except:
		raise ValidationError((f"{value} is not a valid url"), params={'value': value})


def validateIP(value):
	validate = validate_ipv46_address
	try:
		validate(value)

	except:
		raise ValidationError((f"{value} is not a valid ip address"), params={'value': value})


def validateDomain(value):
	try:
		if not re.fullmatch(REGEX_DOMAIN, value):
			raise ValidationError((f"{value} is not a valid domain"), params={'value': value})

	except:
		raise ValidationError((f"{value} is not a valid domain"), params={'value': value})


def validateIP_Domain(value):
	validate_ip = validate_ipv46_address
	try:
		validate_ip(value)
	
	except:
		if not re.fullmatch(REGEX_DOMAIN, value):
			raise ValidationError((f"{value} is not a valid ip address / domain"), params={'value': value})


def validateIP_Domain_URL(value):
	validate_ip = validate_ipv46_address
	validate_url = URLValidator(schemes=["http", "https"])
	try:
		validate_ip(value)
	
	except:
		try:
			validate_url(value)
		
		except:
			if not re.fullmatch(REGEX_DOMAIN, value):
				raise ValidationError((f"{value} is not a valid url / ip address / domain"), params={'value': value})


class StringArrayField(ListField):
	"""
	String representation of an array field.
	"""
	def to_representation(self, obj):
		obj = super().to_representation(self, obj)
		# convert list to string
		return ",".join([str(element) for element in obj])	
	
	def to_internal_value(self, data):
		data = data[0].split(",")  # convert string to list
		return super().to_internal_value(data=data)