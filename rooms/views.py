from django.http import request
from django.http.response import JsonResponse
from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import HttpRequest

from rooms.models import Room
from rooms.serializers import RoomSerializer, CreateRoomSerializer


class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class UserInRoom(APIView):
    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        data = {"code": self.request.session.get("roomCode")}
        return JsonResponse(data=data, status=status.HTTP_200_OK)


class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer

    def post(self, request: HttpRequest, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get("guest_can_pause")
            votes_to_skip = serializer.data.get("votes_to_skip")
            host = self.request.session.session_key
            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                room: Room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=["guest_can_pause", "votes_to_skip"])
            else:
                room: Room = Room(
                    host=host,
                    guest_can_pause=guest_can_pause,
                    votes_to_skip=votes_to_skip,
                )
                room.save()

            self.request.session["roomCode"] = room.code

            return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)


class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = "code"

    def get(self, request: HttpRequest, format=None):
        code: str = request.GET.get(self.lookup_url_kwarg)
        if code:
            room = Room.objects.filter(code=code)
            if len(room) > 0:
                data: dict = RoomSerializer(room[0]).data
                data["is_host"] = self.request.session.session_key == room[0].host
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"Room Not Found": "Invalid Room Code."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"Bad Request": "Missing Code parameter in request"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class JoinRoom(APIView):
    lookup_url_kwarg = "code"

    def post(self, request: HttpRequest, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        code = request.data.get(self.lookup_url_kwarg)
        print(request.data)
        if code:
            roomQS = Room.objects.filter(code=code)
            if len(roomQS) > 0:
                room = roomQS[0]
                self.request.session["roomCode"] = code
                return Response({"message": "Room joined"}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"Bad Request": "Invalid Room Code."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"Bad Request": "Missing Code parameter in request"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LeaveRoom(APIView):
    def post(self, request: HttpRequest, format=None):
        if "roomCode" in self.request.session:
            del self.request.session["roomCode"]
            hostId: str = self.request.session.session_key
            roomQS = Room.objects.filter(host=hostId)
            if len(roomQS) > 0:
                room: Room = roomQS[0]
                room.delete()

        return Response(
            {"message": "Room left"},
            status=status.HTTP_200_OK,
        )
