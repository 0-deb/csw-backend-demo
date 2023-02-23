from rest_access_policy import AccessPolicy
from Users.models import Permissions, UserPermissions
from Billing.models import OrganizationPackages, Packages

# @decorators.permission_classes([UserPermission & GroupPermission])
# @decorators.permission_classes((UserPermission | GroupPermission,)) NOTE: For using OR operations

class IsAdminOrSuperAdmin(AccessPolicy):
    statements = [
        {
            "action": ["*"],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": "is_admin"         
        },
        {
            "action": ["*"],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": "is_superuser"         
        }
    ]


    def is_admin(self, request, view, action) -> bool:
        if request.user.is_authenticated:
            return request.user.is_admin
        else:
            return False


    def is_superuser(self, request, view, action) -> bool:
        if request.user.is_authenticated:
            return request.user.is_superuser
        else:
            return False


class IsSuperAdmin(AccessPolicy):
    statements = [
        {
            "action": ["*"],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": "is_superuser"         
        }
    ]


    def is_superuser(self, request, view, action) -> bool:
        if request.user.is_authenticated:
            return request.user.is_superuser
        else:
            return False


class IsAdminUser(AccessPolicy):
    statements = [
        {
            "action": ["*"],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": "is_adminuser"         
        }
    ]


    def is_adminuser(self, request, view, action) -> bool:
        if request.user.is_authenticated:
            return request.user.is_admin
        else:
            return False


class GroupPermission(AccessPolicy):
    statements = [
        {
            "action": ["*"],
            "principal": ["group:Administrator"],
            "effect": "allow"            
        }
    ]

    # def get_user_group_values(self, user) -> List[str]:
    #     groups = list(user.groups.values_list("name", flat=True))
    #     return groups


    def is_admin(self, request, view, action) -> bool:
        if request.user.is_authenticated:
            return request.user.is_admin
        else:
            return False


class ScannerREAD(AccessPolicy):
    statements = [
        {
            "action": ["*"],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": "is_authorized"
        }
    ]

    def is_authorized(self, request, view, action) -> bool:
        try:
            OrganizationPackagesData = OrganizationPackages.objects.get(OrganizationID = request.user.Organization.OrganizationID, Package = Packages.objects.get(PackageCodename = "Scanner_Package")) # TODO: Change accordingly before testing / production.

            if OrganizationPackagesData:
                    UserPermissionsData = UserPermissions.objects.get(UserID = request.user.UserID, Permission = Permissions.objects.get(PermissionCodename = "Scanner_Feature_READ"))
                    if UserPermissionsData:
                        return True

        except:
            pass
            
        return False


class ScannerWRITE(AccessPolicy):
    statements = [
        {
            "action": ["*"],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": "is_authorized"
        }
    ]

    def is_authorized(self, request, view, action) -> bool:
        try:
            OrganizationPackagesData = OrganizationPackages.objects.get(OrganizationID = request.user.Organization.OrganizationID, Package = Packages.objects.get(PackageCodename = "Scanner_PACKAGE")) # TODO: Change accordingly before testing / production.

            if OrganizationPackagesData:
                    UserPermissionsData = UserPermissions.objects.get(UserID = request.user.UserID, Permission = Permissions.objects.get(PermissionCodename = "Scanner_Feature_WRITE"))
                    if UserPermissionsData:
                        return True

        except:
            pass
            
        return False


class ScannerDELETE(AccessPolicy):
    statements = [
        {
            "action": ["*"],
            "principal": ["authenticated"],
            "effect": "allow",
            "condition": "is_authorized"
        }
    ]

    def is_authorized(self, request, view, action) -> bool:
        try:
            OrganizationPackagesData = OrganizationPackages.objects.get(OrganizationID = request.user.Organization.OrganizationID, Package = Packages.objects.get(PackageCodename = "Scanner_Package"))

            if OrganizationPackagesData:
                    UserPermissionsData = UserPermissions.objects.get(UserID = request.user.UserID, Permission = Permissions.objects.get(PermissionCodename = "Scanner_DELETE"))
                    if UserPermissionsData:
                        return True

        except:
            pass
            
        return False