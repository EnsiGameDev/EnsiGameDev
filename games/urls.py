from django.urls import path
from . import views

app_name = "games"
urlpatterns = [
    path("<int:game_id>", views.detail, name="detail"),
    path("<str:file_name>", views.serve_static, name='serve_static'),
    path("",views.list,name="list")
]