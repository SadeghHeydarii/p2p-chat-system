from django.urls import path
from .views import register, peers, peerinfo, create_message, start_friendship, get_friends, get_messages

urlpatterns = [
    path("register", register),
    path("peers", peers),
    path("peerinfo", peerinfo),
    path("message/create/", create_message),
    path("message/get/", get_messages),
    path("friend/start/", start_friendship),
    path("friend/get/", get_friends),
]
