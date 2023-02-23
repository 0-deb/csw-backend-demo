

from django.http.response import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework import decorators, permissions
from rest_framework import generics

import Cars.schema as Schema
import Cars.models as carModels 
import Cars.serializers as carSerializers 

from Server.Logging import ExceptionMessage
from Server.Filter import Filter
from Server.Paginator import Paginator
from Server.models import ACTION, ACTIVITIES

import datetime
import hashlib
import random


@Schema.AddBrands
@api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def AddBrand(request):
	try:
		brandDetails = carSerializers.ValidateBrands(data = request.data)
		if not brandDetails.is_valid():
			return JsonResponse({"message": "ValidationError!", "data": {"details": brandDetails.errors}}, status = status.HTTP_406_NOT_ACCEPTABLE)
		
		brandDetails.save()

		return JsonResponse({"message": "Success!", "data": {"id": brandDetails.instance.id}}, status = status.HTTP_200_OK)

	except Exception as e:
		return JsonResponse({"message": ExceptionMessage("Invalid Data!", errorMessage = str(e)), "data": {}}, status = status.HTTP_400_BAD_REQUEST)


@Schema.AddCars
@api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def AddCars(request):
	try:
		try:
			brandDetails = carModels.Brands.objects.get(id = request.data["brandID"])
		except ObjectDoesNotExist:
			return JsonResponse({"message": "Invalid Data!", "data": {"details": "Invalid brand ID"}}, status = status.HTTP_406_NOT_ACCEPTABLE)

		error = {}
		success = []
		for cars in request.data["Cars"]:
			carDetails = carSerializers.ValidateCars(data = {
				"brand": brandDetails.id,
				"model": cars["model"],
				"image": cars["image"],
				"type": cars["type"]
			})
			if not carDetails.is_valid():
				error.update(host = carDetails.errors)
				continue
			
			carDetails.save()
			data = {
				"brandID": carDetails.data["brand"],
				"model": carDetails.validated_data["model"]
			}
			success.append(data)

		return JsonResponse({"message": "Success!", "data": {"details": error}}, status = status.HTTP_200_OK)

	except Exception as e:
		return JsonResponse({"message": ExceptionMessage("Invalid Data!", errorMessage = str(e)), "data": {}}, status = status.HTTP_400_BAD_REQUEST)


@decorators.permission_classes([permissions.AllowAny,])
class ViewBrands(generics.GenericAPIView):
	@Schema.ViewBrands
	@action(detail=True, methods=["get"],)	
	def get(self, request):
		try:
			allBrands = carModels.Brands.objects.all()

			# Data filtering and searching
			filterData = Filter.SearchAndFilter(
				self = self,
				FilterFields=[],
				Query_Set = allBrands,
				SearchFields = ["^name",]
			)

			# Data pagination
			PaginatedData = Paginator.Paginate(
				self = self,
				FilteredQueryset=filterData,
				request = request
			)

			listBrands = []
			for brand in PaginatedData.data["results"]:
				Brand = dict()
				Brand["id"] = brand.id
				Brand["name"] = brand.name
				Brand["logo"] = brand.logo

				listBrands.append(Brand)

			return JsonResponse({
				"message": "Success!", 
				"data": {
					"Count": PaginatedData.data["count"],
					"Next": PaginatedData.data["next"],
					"Previous": PaginatedData.data["previous"],
					"Brands": listBrands
				}
			}, status = status.HTTP_200_OK)

		except Exception as e:
			return JsonResponse({"message": ExceptionMessage("Invalid Data!", errorMessage = str(e)), "data": {}}, status = status.HTTP_400_BAD_REQUEST)


@decorators.permission_classes([permissions.AllowAny,])
class ViewCars(generics.GenericAPIView):
	@Schema.ViewCars
	@action(detail=True, methods=["get"],)	
	def get(self, request):
		try:
			allCars = carModels.Cars.objects.all().select_related("brand")

			# Data filtering and searching
			filterData = Filter.SearchAndFilter(
				self = self,
				Query_Set = allCars,
				FilterFields = ["brand",],
				SearchFields = ["^brand__name", "^model", "type"]
			)

			# Data pagination
			PaginatedData = Paginator.Paginate(
				self = self,
				FilteredQueryset=filterData,
				request = request
			)

			listCars = []
			for car in PaginatedData.data["results"]:
				Car = dict()
				Car["id"] = car.id
				Car["brand"] = car.brand.name
				Car["logo"] = car.brand.logo
				Car["model"] = car.model
				Car["image"] = car.image
				Car["type"] = car.type

				listCars.append(Car)

			return JsonResponse({
				"message": "Success!", 
				"data": {
					"Count": PaginatedData.data["count"],
					"Next": PaginatedData.data["next"],
					"Previous": PaginatedData.data["previous"],
					"Cars": listCars
				}
			}, status = status.HTTP_200_OK)

		except Exception as e:
			return JsonResponse({"message": ExceptionMessage("Invalid Data!", errorMessage = str(e)), "data": {}}, status = status.HTTP_400_BAD_REQUEST)


@Schema.AddOrder
@api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def AddOrder(request):
	try:
		brandDetails = carSerializers.ValidateOrders(data = request.data)
		if not brandDetails.is_valid():
			return JsonResponse({"message": "ValidationError!", "data": {"details": brandDetails.errors}}, status = status.HTTP_406_NOT_ACCEPTABLE)
		
		brandDetails.save()

		return JsonResponse({"message": "Success!", "data": {"id": brandDetails.instance.id}}, status = status.HTTP_200_OK)

	except Exception as e:
		return JsonResponse({"message": ExceptionMessage("Invalid Data!", errorMessage = str(e)), "data": {}}, status = status.HTTP_400_BAD_REQUEST)


@decorators.permission_classes([permissions.AllowAny,])
class ViewOrders(generics.GenericAPIView):
	@Schema.ViewOrders
	@action(detail=True, methods=["get"],)	
	def get(self, request):
		try:
			allOrders = carModels.Orders.objects.all().select_related("car")

			# Data filtering and searching
			filterData = Filter.SearchAndFilter(
				self = self,
				FilterFields=[],
				Query_Set = allOrders,
				SearchFields = ["^name", "^email", "^car__model", "^car__brand__name"]
			)

			# Data pagination
			PaginatedData = Paginator.Paginate(
				self = self,
				FilteredQueryset=filterData,
				request = request
			)

			listOrders = []
			for order in PaginatedData.data["results"]:
				Order = dict()
				Order["id"] = order.id
				Order["name"] = order.name
				Order["email"] = order.email
				Order["carDetails"] = {
					"model": order.car.model,
					"image": order.car.image,
					"brand": order.car.brand.name,
					"logo": order.car.brand.logo,
				}
				Order["serviceList"] = order.serviceList
				Order["dateTime"] = order.dateTime

				listOrders.append(Order)

			return JsonResponse({
				"message": "Success!", 
				"data": {
					"Count": PaginatedData.data["count"],
					"Next": PaginatedData.data["next"],
					"Previous": PaginatedData.data["previous"],
					"Orders": listOrders
				}
			}, status = status.HTTP_200_OK)

		except Exception as e:
			return JsonResponse({"message": ExceptionMessage("Invalid Data!", errorMessage = str(e)), "data": {}}, status = status.HTTP_400_BAD_REQUEST)