from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

from main.views import PopularRestaurantsListView, RestaurantDetailView, \
    DishListView, CuisineTypeListView, CityListView, profile_info_page, ProfileUpdateView, ReviewCreateView

app_name = "main"

urlpatterns = [
    path("", PopularRestaurantsListView.as_view(), name="main"),
    path("restaurant/<int:pk>/", RestaurantDetailView.as_view(), name="restaurant"),
    path("restaurant/<int:pk>/menu/", DishListView.as_view(), name="menu"),
    path("cousins/", CuisineTypeListView.as_view(), name="cuisines"),
    path("cities/", CityListView.as_view(), name="cities"),
    path('profile/<int:id>/', profile_info_page, name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name="edit_profile"),
    path('restaurant/<int:pk>/review-create/', ReviewCreateView.as_view(), name="create_review"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
