from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status

from Server.SwaggerSchema import SWAGGER_SCHEMA


# API documentation | tags = ["Authentication"]

VerifySession = swagger_auto_schema(tags = ["Authentication"], method = "get",
	responses = {
		status.HTTP_200_OK: openapi.Schema(type = openapi.TYPE_OBJECT, properties = {
			"message": openapi.Schema(type = openapi.TYPE_STRING, description = "Success Message!"),
			"data": openapi.Schema(type = openapi.TYPE_OBJECT, description = "Response Data", properties = {
				"user": openapi.Schema(type = openapi.TYPE_OBJECT, properties = {
					"email": openapi.Schema(type = openapi.TYPE_STRING, description = "User email"),
					"username": openapi.Schema(type = openapi.TYPE_STRING, description = "Username"),
					"otp_required": openapi.Schema(type = openapi.TYPE_BOOLEAN, description = "MultiFA status"),
					"admin_user": openapi.Schema(type = openapi.TYPE_BOOLEAN, description = "is_admin status")
				})
			})
		}),
		status.HTTP_403_FORBIDDEN: SWAGGER_SCHEMA.RESPONSE_403,
		status.HTTP_406_NOT_ACCEPTABLE: SWAGGER_SCHEMA.RESPONSE_406
	})

Login = swagger_auto_schema(tags = ["Authentication"], method = "post", request_body = openapi.Schema(type = openapi.TYPE_OBJECT, 
	properties = {
		"email": openapi.Schema(type = openapi.TYPE_STRING, description = "Login Email"),
		"password": openapi.Schema(type = openapi.TYPE_STRING, description = "Login Password"),
	}),
	responses = {
		status.HTTP_200_OK: openapi.Schema(type = openapi.TYPE_OBJECT, properties = {
			"message": openapi.Schema(type = openapi.TYPE_STRING, description = "Success Message!"),
			"data": openapi.Schema(type = openapi.TYPE_OBJECT, description = "Response Data", properties = {
				"Token": openapi.Schema(type = openapi.TYPE_STRING, description = "Bearer Token"),
				"user": openapi.Schema(type = openapi.TYPE_OBJECT, properties = {
					"email": openapi.Schema(type = openapi.TYPE_STRING, description = "User email"),
					"username": openapi.Schema(type = openapi.TYPE_STRING, description = "Username"),
					"otp_required": openapi.Schema(type = openapi.TYPE_BOOLEAN, description = "MultiFA status"),
					"admin_user": openapi.Schema(type = openapi.TYPE_BOOLEAN, description = "is_admin status")
				})
			})
		}),
		status.HTTP_400_BAD_REQUEST: SWAGGER_SCHEMA.RESPONSE_400,
		status.HTTP_401_UNAUTHORIZED: SWAGGER_SCHEMA.RESPONSE_401,
		status.HTTP_403_FORBIDDEN: SWAGGER_SCHEMA.RESPONSE_403,
		status.HTTP_406_NOT_ACCEPTABLE: SWAGGER_SCHEMA.RESPONSE_ERROR_406
	})

Logout = swagger_auto_schema(tags = ["Authentication"], method = "post", responses = {
		status.HTTP_200_OK: SWAGGER_SCHEMA.RESPONSE_200
	})

AppLogout = swagger_auto_schema(tags = ["Authentication"], method = "post", responses = {
		status.HTTP_200_OK: SWAGGER_SCHEMA.RESPONSE_200
	})

ResendEmailVerification = swagger_auto_schema(tags = ["Authentication"], method = "post", request_body = openapi.Schema(type = openapi.TYPE_OBJECT, properties = {
		"email": openapi.Schema(type = openapi.TYPE_STRING, description = "Email address of the user."),
	}),
	responses = {
		status.HTTP_200_OK: SWAGGER_SCHEMA.RESPONSE_200,
		status.HTTP_400_BAD_REQUEST: SWAGGER_SCHEMA.RESPONSE_400,
		status.HTTP_406_NOT_ACCEPTABLE: SWAGGER_SCHEMA.RESPONSE_406
	})

ResetPasswordLink = swagger_auto_schema(tags = ["Authentication"], method = "post", request_body = openapi.Schema(type = openapi.TYPE_OBJECT, properties = {
		"email": openapi.Schema(type = openapi.TYPE_STRING, description = "Email address of the user."),
	}),
	responses = {
		status.HTTP_200_OK: SWAGGER_SCHEMA.RESPONSE_200,
		status.HTTP_400_BAD_REQUEST: SWAGGER_SCHEMA.RESPONSE_400,
		status.HTTP_406_NOT_ACCEPTABLE: SWAGGER_SCHEMA.RESPONSE_406
	})

ResetPassword = swagger_auto_schema(tags = ["Authentication"], method = "post", request_body = openapi.Schema(type = openapi.TYPE_OBJECT, properties = {
		"email": openapi.Schema(type = openapi.TYPE_STRING, description = "Email address of the user."),
		"token": openapi.Schema(type = openapi.TYPE_STRING, description = "Verification token"),
		"password": openapi.Schema(type = openapi.TYPE_STRING, description = "New password of the user"),
		"password2": openapi.Schema(type = openapi.TYPE_STRING, description = "Confirm password"),
	}),
	responses = {
		status.HTTP_200_OK: SWAGGER_SCHEMA.RESPONSE_200,
		status.HTTP_400_BAD_REQUEST: SWAGGER_SCHEMA.RESPONSE_400,
		status.HTTP_403_FORBIDDEN: SWAGGER_SCHEMA.RESPONSE_403,
		status.HTTP_406_NOT_ACCEPTABLE: SWAGGER_SCHEMA.RESPONSE_406
	})

VerifyResetPasswordLink = swagger_auto_schema(tags = ["Authentication"], method = "get", manual_parameters = [
		openapi.Parameter(name = "email", type = openapi.TYPE_STRING, in_=openapi.IN_QUERY, description = "Email address of the user"),
		openapi.Parameter(name = "token", type = openapi.TYPE_STRING, in_=openapi.IN_QUERY, description = "Verification token"),
	],
	responses = {
		status.HTTP_200_OK: SWAGGER_SCHEMA.RESPONSE_200,
		status.HTTP_400_BAD_REQUEST: SWAGGER_SCHEMA.RESPONSE_400,
		status.HTTP_403_FORBIDDEN: SWAGGER_SCHEMA.RESPONSE_403
	})


# API documentation | tags = ["Users & Organizations"]

CreateUser = swagger_auto_schema(tags = ["Users & Organizations"], method = "post", request_body = openapi.Schema(type = openapi.TYPE_OBJECT, 
	properties = {
		"email": openapi.Schema(type = openapi.TYPE_STRING, description = "Login Email"),
		"FirstName": openapi.Schema(type = openapi.TYPE_STRING, description = "First Name"),
		"LastName": openapi.Schema(type = openapi.TYPE_STRING, description = "Last Name"),
		"password": openapi.Schema(type = openapi.TYPE_STRING, description = "Password"),
		"password2": openapi.Schema(type = openapi.TYPE_STRING, description = "Password Confirmation"),
	}),
	responses = {
		status.HTTP_201_CREATED: openapi.Schema(type = openapi.TYPE_OBJECT, properties = {
			"message": openapi.Schema(type = openapi.TYPE_STRING, description = "Success Message!"),
			"data": openapi.Schema(type = openapi.TYPE_OBJECT, description = "Response Data", properties = {
				"email": openapi.Schema(type = openapi.TYPE_STRING, description = "Login Email"),
				"password" : openapi.Schema(type = openapi.TYPE_STRING, description = "Password"),
				"FirstName": openapi.Schema(type = openapi.TYPE_STRING, description = "First Name"),
				"LastName": openapi.Schema(type = openapi.TYPE_STRING, description = "Last Name"),
				"Organization": openapi.Schema(type = openapi.TYPE_NUMBER, description = "Organization ID"),
				"MultiFA": openapi.Schema(type = openapi.TYPE_BOOLEAN, description = "MFA Status")
			})
		}),
		status.HTTP_400_BAD_REQUEST: SWAGGER_SCHEMA.RESPONSE_400,
		status.HTTP_406_NOT_ACCEPTABLE: SWAGGER_SCHEMA.RESPONSE_406
	})