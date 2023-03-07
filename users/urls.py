from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', register, name="register"),
    path('login/', loginView, name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),

]
