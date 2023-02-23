from django.urls import include, re_path
from . import views 


urlpatterns = [ 
    # Authentication
    
    re_path(r'^verify-session$', views.VerifySession),
    re_path(r'^login$', views.Login.as_view()),
    # re_path(r'^logout$', views.Logout.as_view()),

    # User Management
    # re_path(r'^create-user$', views.CreateUser)
]