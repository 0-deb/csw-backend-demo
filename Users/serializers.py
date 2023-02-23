from rest_framework import serializers, exceptions
from .models import UserManager, User
from django.contrib.auth import authenticate
from Server.Validators import StringArrayField


class ValidateCreateUser(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'password2',
            'FirstName',
            'LastName',
            'MultiFA'
        )


    def validate(self,data):

        password = data.get("password")
        password2 = data.pop("password2")

        if password != password2:
            msg = "Password didn't match"
            raise exceptions.NotAcceptable(msg)

        return data


class ValidateCreateAdminUser(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = (  
            'email',
            'password',
            'password2',
            'FirstName',
            'LastName',
            'MultiFA',
            'is_admin'
        )

    def validate(self,data):

        password = data.get("password")
        password2 = data.pop("password2")

        if password != password2:
            msg = "Password didn't match"
            raise exceptions.ValidationError(msg)

        return data


class ValidateLogin(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self,data):
        email = data.get("email","")
        password = data.get("password","")

        if email and password:
            user = authenticate(username=email,password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "User is deactivated."
                    raise exceptions.ValidationError({"message": msg})
            else:
                msg = "Please check your username and password."
                raise exceptions.ValidationError({"message": msg})
        else:
            msg = "Must provide username and password."
            raise exceptions.ValidationError({"message": msg})

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "FirstName",
            "LastName",
            "MultiFA",
            "is_admin"
        )
        
        extra_kwargs = {
            "email":{"required": False},
            "password":{"required": False},
            "password2":{"required": False},
            "FirstName":{"required": False},
            "LastName":{"required": False},
            "MultiFA":{"required": False},
            "is_admin":{"required": False}    
        }