""" URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  re_path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  re_path(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  re_path(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, re_path
from django.contrib.auth.decorators import permission_required

from drf_yasg.views import get_schema_view 
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator

from rest_framework import permissions


USER_URL = re_path(r'^user/', include('Users.urls'))
CAR_URL = re_path(r'^car/', include('Cars.urls'))

user_schema_view = get_schema_view( 
    openapi.Info(
        title="User API", 
        default_version='v1', 
        description="User API Documentation", 
        terms_of_service="https://www.google.com/policies/terms/", 
        contact=openapi.Contact(email="admin@jabotics.in"), 
        license=openapi.License(name="BSD License"), 
    ),
    public=True,
    patterns=[USER_URL],
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,), 
)

car_schema_view = get_schema_view( 
    openapi.Info(
        title="Cars API", 
        default_version='v1', 
        description="User API Documentation", 
        terms_of_service="https://www.google.com/policies/terms/", 
        contact=openapi.Contact(email="admin@jabotics.in"), 
        license=openapi.License(name="BSD License"), 
    ),
    public=True,
    patterns=[CAR_URL],
    permission_classes=[permissions.AllowAny] 
)

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    
    # API
    USER_URL,
    CAR_URL,
    
    # REDOC DOCUMENTATION
    re_path(r'^user/docs/$', permission_required('schema-redoc')(user_schema_view.with_ui('redoc', cache_timeout=0)), name = 'schema-redoc'),
    re_path(r'^carr/docs/$', permission_required('schema-redoc')(car_schema_view.with_ui('redoc', cache_timeout=0)), name = 'schema-redoc'),
    
    # SWAGGER DOCUMENTATION
    re_path(r'^user/playground/$', user_schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^car/playground/$', car_schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]