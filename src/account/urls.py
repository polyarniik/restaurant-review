from django.urls import path

from account.views import MyLoginView, RegisterView, MyLogoutView

app_name = "account"

urlpatterns = [
    path("login/", MyLoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
]
