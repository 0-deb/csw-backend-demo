from django.contrib import admin
from .models import Brands, Cars, Orders


class BrandsAdmin(admin.ModelAdmin):
	model = Brands
	list_display = ("id", "name", "logo")
	list_display_links = ("id",)
	search_fields = ("name", "logo")
	readonly_fields = ("id",)
	
	fieldsets = (
		("ConstantFields", {"fields": ("id",)}),
		("ChangeableFields", {"fields": ("name", "logo")})
	)

class CarsAdmin(admin.ModelAdmin):
	model = Cars
	list_display = ("id", "brand", "model", "type", "image")
	list_display_links = ("id",)
	list_filter = ("type",)
	search_fields = ("brand__name", "brand__logo", "model", "image")
	readonly_fields = ("id",)
	
	fieldsets = (
		("ConstantFields", {"fields": ("id",)}),
		("ChangeableFields", {"fields": ("brand", "model", "type", "image")})
	)

	def __str__(self, obj):
		return obj.brand.name

class OrdersAdmin(admin.ModelAdmin):
	model = Orders
	list_display = ("id", "car_brand", "car_model", "name", "email", "service_list", "dateTime")
	
	list_display_links = ("id",)
	list_filter = ("car__brand", "car__type")
	search_fields = ("car__model", "car__type", "car__brand__name")
	readonly_fields = ("id",)
	
	fieldsets = (
		("ConstantFields", {"fields": ("id",)}),
		("ChangeableFields", {"fields": ("name", "email", "car", "serviceList", "dateTime")})
	)

	def __str__(self, obj):
		return obj.id

	@admin.display(ordering='car', description='Brand')
	def car_brand(self, obj):
		return obj.car.brand.name

	@admin.display(ordering='car', description='Model')
	def car_model(self, obj):
		return obj.car.model

	@admin.display(ordering='car', description='ServiceList')
	def service_list(self, obj):
		allServices = ""
		for i in obj.serviceList:
			if int(i) == len(obj.serviceList) - 1:
				allServices = f"{allServices} {obj.serviceList[i]['name']}"
				continue

			if len(allServices) == 0:
				allServices = f"{obj.serviceList[i]['name']},"
				continue
			
			allServices = f"{allServices} {obj.serviceList[i]['name']},"

		return allServices


admin.site.register(Cars, CarsAdmin)
admin.site.register(Brands, BrandsAdmin)
admin.site.register(Orders, OrdersAdmin)