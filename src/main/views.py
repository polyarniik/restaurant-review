import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView

from main.forms import ProfileEditForm, ReviewModelForm
from main.models import Restaurant, Dish, CuisineType, City, Profile, Review

User = get_user_model()


class PopularRestaurantsListView(generic.ListView):
    model = Restaurant
    template_name = "main/index.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super(PopularRestaurantsListView, self).get_context_data()
        if "by" not in self.request.GET:
            context_data["page_tittle"] = "Самые популярные рестораны"
        elif "all" in self.request.GET:
            context_data["page_tittle"] = "Все рестораны"
        elif self.request.GET["by"] == "city" and self.request.GET["id"]:
            city = get_object_or_404(City, pk=(self.request.GET["id"]))
            context_data["page_tittle"] = "Рестораны города " + city.name
        elif self.request.GET["by"] == "cuisine" and self.request.GET["id"]:
            cuisine = get_object_or_404(CuisineType, pk=(self.request.GET["id"]))
            context_data["page_tittle"] = "Рестораны по запросу: " + cuisine.name
        return context_data

    def get_queryset(self):
        if "all" in self.request.GET:
            return Restaurant.objects.all()
        if "by" not in self.request.GET:
            return Restaurant.objects.all()[:4]
        elif "id" in self.request.GET:
            if self.request.GET["by"] == "city":
                return Restaurant.objects.filter(city_id=self.request.GET["id"])
            elif self.request.GET["by"] == "cuisine":
                return Restaurant.objects.filter(cuisine_type_id=self.request.GET["id"])
            else:
                return Restaurant.objects.all()[:4]
        else:
            return Restaurant.objects.all()[:4]


class RestaurantDetailView(generic.DetailView):
    model = Restaurant
    template_name = "main/restaurant.html"


class DishListView(generic.ListView):
    model = Dish
    template_name = "main/menu.html"

    def get_queryset(self):
        return Dish.objects.filter(restaurant_id=self.kwargs["pk"]).order_by("price")


class CuisineTypeListView(generic.ListView):
    model = CuisineType
    template_name = 'main/cousins.html'


class CityListView(generic.ListView):
    model = City
    template_name = "main/cities.html"


def profile_info_page(request, id):
    profile = get_object_or_404(Profile, user_id=id)
    return render(request, "main/profile.html", context={
        "profile": profile
    })


class ProfileUpdateView(generic.UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'main/edit-profile.html'

    def get_success_url(self):
        return reverse_lazy("main:profile", kwargs={"id": self.request.user.id})

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

    def get_queryset(self):
        return Profile.objects.get_queryset()


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    http_method_names = ['post', 'get']
    form_class = ReviewModelForm
    template_name = 'main/create-review.html'

    def get_success_url(self):
        return reverse_lazy("main:restaurant",
                            kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            form.instance.restaurant_id = self.kwargs["pk"]
            # form.instance.date = datetime.datetime.now()
        return super(ReviewCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return redirect("main:restaurant", pk=self.kwargs["pk"])

    def post(self, *args, **kwargs):
        print("here")
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
