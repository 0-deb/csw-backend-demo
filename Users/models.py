from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.contrib.postgres.fields import ArrayField

# S3 Storage Imports
from Server.Validators import validateURL
from Server.Utils import EnumChoices

from Core import settings
from datetime import datetime, timedelta
import jwt


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`. 
    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, email, password, FirstName, LastName):
        """Create and return a `User` with an email, username and password."""

        if not email:
            raise TypeError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email))
        user.FirstName = FirstName
        user.LastName = LastName
        user.set_password(password)
        user.save()

        return user


    def create_superuser(self,  email, password, FirstName, LastName):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password, FirstName, LastName)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    UserID = models.BigAutoField(primary_key=True)
    email = models.EmailField(blank=False, unique=True, db_index=True)
    password = models.CharField(blank=False,max_length=200)
    FirstName = models.CharField(blank=False,max_length=25)
    LastName = models.CharField(blank=False,max_length=25)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case we want it to be the email field.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['FirstName', 'LastName']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.
        This string is used when a `User` is printed in the console.
        """
        return self.email

    def token(self, request):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().
        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token(request=request)


    def OTPToken(self, request, otp_verified=False):
        return self._generate_jwt_token(request=request, otp_verified=otp_verified)


    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically this would be the user's first and last name. Since we do
        not store the user's real name, we return their username instead.
        """
        return f"{self.FirstName} {self.LastName}"


    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name. Since we do not store
        the user's real name, we return their username instead.
        """
        return self.FirstName


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True


    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


    def has_change_permission(self, request, obj=None):
        return True


    def has_delete_permission(self, request, obj=None):
        return True


    def _generate_jwt_token(self, request, otp_verified=False):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to days into the future.
        """
        dt = datetime.utcnow() + timedelta(days=settings.JWT_Expiration_Duration)
        receiveToken = request.auth
        payload = dict() # palyload.get() method can't be done in None type objects
        if receiveToken:
            payload = jwt.decode(receiveToken, settings.SECRET_KEY, algorithms='HS256')

        token = {
            'UserID': self.pk,
            'Expire': int(dt.strftime('%s'))
        }

        if self.MultiFA:
            token["OTPVerified"] = otp_verified
        
        encodedToken = jwt.encode(token, settings.SECRET_KEY, algorithm='HS256')
        
        return encodedToken


class BlacklistToken(models.Model):
    JWToken = models.TextField(blank=False)
    User = models.ForeignKey(User,db_column="UserID",on_delete=models.CASCADE)
    BlacklistDate = models.DateTimeField(auto_now_add=True)
    ExpirationDate = models.DateTimeField()

    class Meta:
        db_table = 'BlacklistedToken'
        managed = True

    def __str__(self):
        return f"{self.User} | {self.JWToken}"


class VERIFICATION_TYPE(EnumChoices):
    EMAIL_VERIFICATION = "Email_Verification"
    PASSWORD_VERIFICATION = "Password_Verification"


class VerificationLink(models.Model):
    ID = models.BigAutoField(primary_key=True)
    User = models.ForeignKey(User, db_column="email", on_delete=models.CASCADE)
    VerificationType = models.CharField(blank=False, choices=VERIFICATION_TYPE.choices(), max_length=100)
    Token = models.TextField(blank=False, unique=True, db_index=True)
    PreviousAttempts = models.IntegerField(default=1)
    ExpirationDate = models.DateTimeField()

    class Meta:
        db_table = 'VerificationLink'
        managed = True

    def __str__(self):
        return f"{self.User} | {self.VerificationType} | {self.ExpirationDate}"