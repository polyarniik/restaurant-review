from django.contrib import admin

from main.models import City, Profile, CuisineType, Reward, Restaurant, Review, Dish


class CityModelAdmin(admin.ModelAdmin):
    list_display = ("name", "photo")
    ordering = ("name",)


class RestaurantModelAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "cuisine_type", "phone", "address", "site", "email")
    list_filter = ("city", "cuisine_type")
    search_fields = ("name", "address", "phone")



admin.site.register(City, CityModelAdmin)
admin.site.register(Profile)
admin.site.register(CuisineType)
admin.site.register(Reward)
admin.site.register(Restaurant, RestaurantModelAdmin)
admin.site.register(Review)
admin.site.register(Dish)
