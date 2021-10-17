from django.contrib import auth
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, RedirectView

from account.forms import RegisterForm, LoginForm
from main.models import Profile


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "main/register.html"
    success_url = "/"

    def form_valid(self, form):
        user = form.save()
        Profile(user=user).save()
        if user is not None:
            return redirect("account:login")
        else:
            form = RegisterForm()
            return render(self.request, self.template_name, context={"form": form})


class MyLoginView(DjangoLoginView):
    authentication_form = LoginForm
    template_name = "main/login.html"
    success_url = reverse_lazy("main:main")
    redirect_authenticated_user = True


class MyLogoutView(RedirectView):
    url = reverse_lazy("main:main")

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return super(MyLogoutView, self).get(request, *args, **kwargs)
