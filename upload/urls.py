from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'upload'

urlpatterns = [
    path('', views.upload, name='upload'),
    path('uploaded/', views.uploaded, name='upload_done')
]