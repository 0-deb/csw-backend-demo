from rest_framework import serializers
from datetime import datetime
import Cars.models as carModels 


class ValidateBrands(serializers.ModelSerializer):

	class Meta:
		model = carModels.Brands
		exclude = ["id"]

		extra_kwargs = {
			"name": {"required": True},
			"logo": {"required": True}
		}


class ValidateCars(serializers.ModelSerializer):

	class Meta:
		model = carModels.Cars
		exclude = ["id"]

		extra_kwargs = {
			"brand": {"required": True},
			"model": {"required": True},
			"image": {"required": True}
		}


class ValidateOrders(serializers.ModelSerializer):

	class Meta:
		model = carModels.Orders
		exclude = ["id"]

		extra_kwargs = {
			"car": {"required": True},
			"name": {"required": True},
			"email": {"required": True},
			"dateTime": {"required": True},
			"serviceList": {"required": True}
		}

	def validate(self, data):
		thisInstance = datetime.utcnow().timestamp()
		inputDatetime = data.get("dateTime").timestamp()
		print(thisInstance)
		print(inputDatetime)
		if inputDatetime <= thisInstance:
			raise serializers.ValidationError({"dateTime": "DateTime field can't be in past"})

		return data