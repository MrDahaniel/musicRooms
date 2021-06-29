from django.urls import path
from frontend import views

urlpatterns = [
    path("", views.index, name="home"),
    path("join", views.index),
    path("create", views.index),
    path("room/<str:roomCode>", views.index),
]
