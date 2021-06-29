from django.urls import path
from rooms import views

urlpatterns = [
    path("", views.RoomView.as_view(), name="RoomView"),
    path("create/room", views.CreateRoomView.as_view(), name="CreateRoomView"),
    path("get/room", views.GetRoom.as_view(), name="GetRoom"),
    path("join/room", views.JoinRoom.as_view(), name="JoinRoom"),
    path("leave/room", views.LeaveRoom.as_view(), name="LeaveRoom"),
    path("user/room", views.UserInRoom.as_view(), name="UserInRoom"),
]
