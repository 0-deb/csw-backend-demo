from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status

from Server.SwaggerSchema import SWAGGER_SCHEMA


# API documentations | tags = ["Add Asset"]

AddBrands = swagger_auto_schema(tags = ["Add"], method = "post", request_body = openapi.Schema(type = openapi.TYPE_OBJECT, properties = {
		"name": openapi.Schema(type = openapi.TYPE_STRING, description = "Name of the brand"),
		"logo": openapi.Schema(type = openapi.TYPE_STRING, description = "Logo of the brand")
	}),
	responses = {
		status.HTTP_200_OK: SWAGGER_SCHEMA.RESPONSE_200,
		status.HTTP_400_BAD_REQUEST: SWAGGER_SCHEMA.RESPONSE_400,
		status.HTTP_406_NOT_ACCEPTABLE: SWAGGER_SCHEMA.RESPONSE_ERROR_406
	})

AddCars = swagger_auto_schema(tags = ["Add"], method = "post", request_body = openapi.Schema(type = openapi.TYPE_OBJECT, properties = {
		"brandID": openapi.Schema(type = openapi.TYPE_NUMBER, description = "Name of the brand"),
		"Cars": openapi.Schema(type = openapi.TYPE_ARRAY, items = openapi.Items(type = openapi.TYPE_OBJECT, properties = {
			"model": openapi.Schema(type = openapi.TYPE_STRING, description = "Name of the brand"),
			"image": openapi.Schema(type = openapi.TYPE_STRING, description = "Logo of the brand"),
			"type": openapi.Schema(type = openapi.TYPE_STRING, description = "Type of vehicle")
		}))
	}),
	responses = {
		status.HTTP_200_OK: SWAGGER_SCHEMA.RESPONSE_200,
		status.HTTP_400_BAD_REQUEST: SWAGGER_SCHEMA.RESPONSE_400,
		status.HTTP_406_NOT_ACCEPTABLE: SWAGGER_SCHEMA.RESPONSE_ERROR_406
	})


AddOrder = swagger_auto_schema(tags = ["Add"], method = "post", request_body = openapi.Schema(type = openapi.TYPE_OBJECT, properties = {
		"car": openapi.Schema(type = openapi.TYPE_NUMBER, description = "ID of the car"),
		"name": openapi.Schema(type = openapi.TYPE_STRING, description = "Name of the user"),
		"email": openapi.Schema(type = openapi.TYPE_STRING, description = "Email of the user"),
		"serviceList": openapi.Schema(type = openapi.TYPE_OBJECT, description = "list of the brand"),
		"dateTime": openapi.Schema(type = openapi.TYPE_STRING, description = "Type of vehicle")
	}),
	responses = {
		status.HTTP_200_OK: SWAGGER_SCHEMA.RESPONSE_200,
		status.HTTP_400_BAD_REQUEST: SWAGGER_SCHEMA.RESPONSE_400,
		status.HTTP_406_NOT_ACCEPTABLE: SWAGGER_SCHEMA.RESPONSE_ERROR_406
	})


ViewBrands = swagger_auto_schema(tags = ["View"], method = "get", manual_parameters = [
		openapi.Parameter("search", in_ = openapi.IN_QUERY, type = openapi.TYPE_STRING, description = "Search keyword"),
	],
	responses = {
		status.HTTP_200_OK: openapi.Schema(type = openapi.TYPE_OBJECT, properties = {
			"message": openapi.Schema(type = openapi.TYPE_STRING, description = "Success Message"),
			"data": openapi.Schema(type = openapi.TYPE_OBJECT, properties = {
				"allBrands": openapi.Schema(type = openapi.TYPE_ARRAY, items =
					openapi.Items(type = openapi.TYPE_OBJECT, properties = {
						"id": openapi.Schema(type = openapi.TYPE_STRING, description = "ID of the brand"),
						"name": openapi.Schema(type = openapi.TYPE_STRING, description = "Name of the brand"),
						"logo": openapi.Schema(type = openapi.TYPE_STRING, description = "Logo of the brand")
					})
				)
			})
		}),
		status.HTTP_400_BAD_REQUEST: SWAGGER_SCHEMA.RESPONSE_400
	})

ViewCars = swagger_auto_schema(tags = ["View"], method = "get", manual_parameters = [
		openapi.Parameter("name", in_ = openapi.IN_QUERY, type = openapi.TYPE_NUMBER, description = "ID of brands"),
		openapi.Parameter("search", in_ = openapi.IN_QUERY, type = openapi.TYPE_STRING, description = "Search keyword"),
	],
	responses = {
		status.HTTP_200_OK: openapi.Schema(type = openapi.TYPE_OBJECT, properties = {
			"message": openapi.Schema(type = openapi.TYPE_STRING, description = "Success Message"),
			"data": openapi.Schema(type = openapi.TYPE_OBJECT, properties = {
				"Count": openapi.Schema(type = openapi.TYPE_NUMBER, description = "Total count of return data"),
				"Next": openapi.Schema(type = openapi.TYPE_STRING, description = "Next URL"),
				"Previous": openapi.Schema(type = openapi.TYPE_STRING, description = "Previous URL"),				
				"Cars": openapi.Schema(type = openapi.TYPE_ARRAY, items = openapi.Items(type = openapi.TYPE_OBJECT, properties = {
						"id": openapi.Schema(type = openapi.TYPE_STRING, description = "ID of the cloud asset"),
						"brand": openapi.Schema(type = openapi.TYPE_STRING, description = "Host of the cloud asset"),
						"logo": openapi.Schema(type = openapi.TYPE_STRING, description = "Name of the host"),
						"model": openapi.Schema(type = openapi.TYPE_STRING, description = "Service type of the cloud asset"),
						"image": openapi.Schema(type = openapi.TYPE_STRING, description = "Region of the cloud asset"),
						"type": openapi.Schema(type = openapi.TYPE_BOOLEAN, description = "If intrusive scan")
					})
				)
			})
		}),
		status.HTTP_400_BAD_REQUEST: SWAGGER_SCHEMA.RESPONSE_400
	})


ViewOrders = swagger_auto_schema(tags = ["View"], method = "get", manual_parameters = [
		openapi.Parameter("search", in_ = openapi.IN_QUERY, type = openapi.TYPE_STRING, description = "Search keyword"),
	],
	responses = {
		status.HTTP_200_OK: openapi.Schema(type = openapi.TYPE_OBJECT, properties = {
			"message": openapi.Schema(type = openapi.TYPE_STRING, description = "Success Message"),
			"data": openapi.Schema(type = openapi.TYPE_OBJECT, properties = {
				"allOrders": openapi.Schema(type = openapi.TYPE_ARRAY, items =
					openapi.Items(type = openapi.TYPE_OBJECT, properties = {
						"id": openapi.Schema(type = openapi.TYPE_STRING, description = "ID of the order"),
						"name": openapi.Schema(type = openapi.TYPE_STRING, description = "Name of the user"),
						"brand": openapi.Schema(type = openapi.TYPE_STRING, description = "Name of the brand"),
						"model": openapi.Schema(type = openapi.TYPE_STRING, description = "Name of the model"),
						"email": openapi.Schema(type = openapi.TYPE_STRING, description = "Email of the user"),
						"dateTime": openapi.Schema(type = openapi.TYPE_STRING, description = "Datetime of the order"),
					})
				)
			})
		}),
		status.HTTP_400_BAD_REQUEST: SWAGGER_SCHEMA.RESPONSE_400
	})