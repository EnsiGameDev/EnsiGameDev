from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'login'

urlpatterns = [
    path('', views.log_in, name='log_in'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]