from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from .forms import UserCreationForm
from .models import User, BlacklistToken, VerificationLink
from django_otp.admin import OTPAdminSite
from django.conf import settings


admin.site.site_header = "SuperAdmin Dashboard"
admin.site.index_title = "Automated Pentest Platform"
admin.site.site_title = "Administrator"
admin.autodiscover()

if not settings.DEBUG:
    admin.site.__class__ = OTPAdminSite # Added OTP authentication to Django Admin


class UserAdministration(UserAdmin):
    model = User
    add_form = UserCreationForm

    list_display = ('email', 'FirstName', 'LastName', 'UserID', 'is_staff', 'is_superuser', 'is_admin', 'is_deleted', 'email_verified')
    search_fields = ('email', 'UserID')
    ordering = ('UserID','email',)
    readonly_fields = ('date_joined', 'last_login', 'UserID')
    exclude = ('username', 'last_name', 'first_name',)
    list_filter = ('is_active', 'is_staff', 'is_superuser','is_admin', 'is_deleted', 'groups')
    # list_editable = ('is_staff','is_superuser')

    fieldsets = (
        ('Personal Info', {'fields': ('UserID', 'FirstName','LastName', 'email', 'password', 'MultiFA', 'email_verified')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'is_staff', 'is_superuser', 'is_deleted', 'groups', 'user_permissions')}),
        ('Audit Log', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        ("User Details", {
            'classes': ('wide','extrapretty'),
            'fields': ('email', 'FirstName', 'LastName', 'password', 'password2', 'MultiFA', 'email_verified')}
        ),
        ("Permissions", {
            'classes': ('wide','extrapretty'),
            'fields': ('is_admin', 'is_staff', 'is_superuser','groups', 'user_permissions')}
        )
    )


class BlacklistedToken(admin.ModelAdmin):
    model = BlacklistToken
    list_display = ('user', 'JWToken', 'BlacklistDate', 'ExpirationDate')
    search_fields = ('User',)
    exclude = ('User',)
    readonly_fields = ('JWToken', 'user', 'BlacklistDate', 'ExpirationDate')
    fieldsets = (
        ('Blacklisted Token', {'fields': ('user', 'JWToken', 'BlacklistDate', 'ExpirationDate')}),
    )

    def user(self, obj):
        return obj.User.email


class AuthTokens(admin.ModelAdmin):
    model = VerificationLink
    list_display = ("User", "VerificationType", "PreviousAttempts", "ExpirationDate")
    search_fields = ("User__email","ExpirationDate", "VerificationType")
    list_display_links = ("User",)
    ordering = ("User", "ExpirationDate", "VerificationType")

    fieldsets = (
        ("VerificationDetails", {"fields": ("User","ExpirationDate","VerificationType", "PreviousAttempts", "Token")}),
    )

    def package(self, obj):
        return obj.AuthenticationToken.User


admin.site.register(User, UserAdministration)
admin.site.register(BlacklistToken, BlacklistedToken)
admin.site.register(VerificationLink, AuthTokens)