from drf_yasg import openapi


class SWAGGER_SCHEMA:
	RESPONSE_200 = openapi.Schema(
		type = openapi.TYPE_OBJECT, 
		properties = {
			"message": openapi.Schema(type = openapi.TYPE_STRING, description = "Success Message"),
			"data": openapi.Schema(type = openapi.TYPE_OBJECT, properties = {})
		})

	RESPONSE_ERROR_200 = openapi.Schema(
		type = openapi.TYPE_OBJECT, 
		properties = {
			"message": openapi.Schema(type = openapi.TYPE_STRING, description = "Success Message"),
			"data": openapi.Schema(type = openapi.TYPE_OBJECT, properties = {
				"error": openapi.Schema(type = openapi.TYPE_ARRAY, items=openapi.Items(
					type=openapi.TYPE_STRING), description = "Error details")
				}
			)
		})

	RESPONSE_400 = openapi.Schema(
		type = openapi.TYPE_OBJECT, 
		properties = {
			"message": openapi.Schema(type = openapi.TYPE_STRING, description = "Error Message"),
			"data": openapi.Schema(type = openapi.TYPE_OBJECT, properties = {})
		})

	RESPONSE_401 = openapi.Schema(
		type = openapi.TYPE_OBJECT, 
		properties = {
			"message": openapi.Schema(type = openapi.TYPE_STRING, description = "Error Message!"),
			"data": openapi.Schema(type = openapi.TYPE_OBJECT, properties = {})
		})

	RESPONSE_403 = openapi.Schema(
		type = openapi.TYPE_OBJECT, 
		properties = {
			"message": openapi.Schema(type = openapi.TYPE_STRING, description = "Error Message!"),
			"data": openapi.Schema(type = openapi.TYPE_OBJECT, properties = {})
		})

	RESPONSE_406 = openapi.Schema(
		type = openapi.TYPE_OBJECT, 
		properties = {
			"message": openapi.Schema(type = openapi.TYPE_STRING, description = "Error Message"),
			"data": openapi.Schema(type = openapi.TYPE_OBJECT, properties = {})
		})

	RESPONSE_ERROR_406 = openapi.Schema(
		type = openapi.TYPE_OBJECT, 
		properties = {
			"message": openapi.Schema(type = openapi.TYPE_STRING, description = "Error Message"),
			"data": openapi.Schema(
				type = openapi.TYPE_OBJECT, 
				properties = {
				"error": openapi.Schema(type = openapi.TYPE_ARRAY, items=openapi.Items(
					type=openapi.TYPE_STRING), description = "Error details")
				}
			)
		})