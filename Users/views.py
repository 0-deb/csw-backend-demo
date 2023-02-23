from django.contrib import auth
from django.contrib.auth.password_validation import validate_password
from django.conf import settings
from django.core import exceptions
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.views.generic.base import View

from rest_framework import generics, status
from rest_framework.decorators import api_view, parser_classes
from rest_framework import decorators, permissions
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser

from django_otp.plugins.otp_static.models import StaticDevice

from .models import User, BlacklistToken, VerificationLink, VERIFICATION_TYPE
from .serializers import ValidateCreateUser, ValidateCreateAdminUser, ValidateLogin, UserSerializer
import Users.schema as Schema
from Users.authentication import ManageIPBlacklist

from Server.models import AuditLogs, AUTHENTICATION_TYPE
from Server.Logging import ExceptionMessage, SerializerErrorMessage

from datetime import datetime, timedelta
from uuid import uuid4
from random import randint

import jwt 
import secrets


@Schema.VerifySession
@api_view(['GET'])
@decorators.permission_classes([permissions.IsAuthenticated])
def VerifySession(request):
	if request.user:
		userDetail = {
			"email": request.user.email, 
			"username": f"{request.user.FirstName} {request.user.LastName}", 
			"otp_required": request.user.MultiFA,
			"admin_user": request.user.is_admin
		}
		return JsonResponse({"message": "Success!", "data": {"user": userDetail}}, status = status.HTTP_200_OK)

	return JsonResponse({"message": "Forbidden!", "data": {}}, status = status.HTTP_403_FORBIDDEN)


@decorators.permission_classes([permissions.AllowAny])
class Login(APIView):
	@Schema.Login
	@action(detail = True, methods = ["post"],)
	def post(self, request):
		try:
			# NOTE: "HTTP_X_FORWARDED_FOR" is for proxy connections and VPNs 
			if request.META.get("HTTP_X_FORWARDED_FOR"):
				ipAddress = request.META["HTTP_X_FORWARDED_FOR"]

			else:
				ipAddress = request.META["REMOTE_ADDR"]

			LoginDetails = ValidateLogin(data = request.data)
			if LoginDetails.is_valid():
				user = LoginDetails.validated_data["user"]

				if not user.email_verified:
					return JsonResponse({"message": "Unauthorized!", "data": {"error": ["Please verify your email address!"]}}, status = status.HTTP_401_UNAUTHORIZED)

				if user.is_deleted:
					return JsonResponse({"message": "ValidationError!", "data": {"error": ["User doesn't exist"]}}, status = status.HTTP_406_NOT_ACCEPTABLE)

				existedBlacklist = ManageIPBlacklist.CheckBlacklist(
					user = user, 
					ipAddress = ipAddress, 
					authType = AUTHENTICATION_TYPE.REST_API.name
				)

				if existedBlacklist:
					msg = "IP address is temporarily blocked, please try after sometime."
					return JsonResponse({"message": "Forbidden!", "data": {"error": [msg]}}, status = status.HTTP_403_FORBIDDEN)

				auth.login(request, user)

				userDetail = {
					"email": user.email, 
					"username": f"{user.FirstName} {user.LastName}", 
					"otp_required": user.MultiFA,
					"admin_user": user.is_admin
				}
				return JsonResponse({"message": "Success!", "data": {"Token": user.token(request), "user": userDetail}}, status = status.HTTP_200_OK)

			else:
				blacklisted = ManageIPBlacklist.ValidateBlacklist(
					email = request.data["email"],
					ipAddress = ipAddress,
					authType = AUTHENTICATION_TYPE.REST_API.name
				)

				if blacklisted:
					msg = "IP address is temporarily blocked, please try after sometime."
					return JsonResponse({"message": "Forbidden!", "data": {"error": [msg]}}, status = status.HTTP_403_FORBIDDEN)

				return JsonResponse({"message": "Forbidden!", "data": {"error": SerializerErrorMessage(LoginDetails.errors)}}, status = status.HTTP_403_FORBIDDEN)

		except Exception as e:
			return JsonResponse({"message": ExceptionMessage("Error while login.", errorMessage=str(e)), "data": {}}, status = status.HTTP_400_BAD_REQUEST)