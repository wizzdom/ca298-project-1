from django.urls import path, include
from . import views
from .forms import * # add o imports at the top of the file
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('',views.index, name="index"),
    path('register/', views.UserSignupView.as_view(), name="register"),
    path('login/',views.LoginView.as_view(template_name="login.html", authentication_form=UserLoginForm)),
    path('logout/', views.logout_user, name="logout"),
    path('orders/', views.orders, name="orders"),
    path('orders/create_pizza/', views.create_pizza, name="create_pizza"),
    path('orders/checkout/', views.checkout, name="checkout"),
    path('orders/confirmation/', views.confirmation, name="confirmation"),
    ]