from django.urls import include, re_path
from . import views 


urlpatterns = [ 
    # Authentication
    
    re_path(r'^add-cars$', views.AddCars),
    re_path(r'^add-orders', views.AddOrder),
    re_path(r'^add-brands$', views.AddBrand),
    re_path(r'^view-cars$', views.ViewCars.as_view()),
    re_path(r'^view-brands$', views.ViewBrands.as_view()),
    re_path(r'^view-orders$', views.ViewOrders.as_view()),

    # User Management
    # re_path(r'^create-user$', views.CreateUser)
]