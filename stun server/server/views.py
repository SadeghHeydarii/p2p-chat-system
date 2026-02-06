import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Peer, Message, Friendship


@csrf_exempt
def create_message(request):
    """
    POST:
    {
        "sender": "alice",
        "receiver": "bob",
        "content": "hello"
    }
    """

    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST allowed"},
            status=405
        )

    try:
        data = json.loads(request.body.decode())
        sender_username = data.get("sender")
        receiver_username = data.get("receiver")
        content = data.get("content")

        if not sender_username or not receiver_username or not content:
            return JsonResponse(
                {"error": "Missing fields"},
                status=400
            )

        sender = Peer.objects.get(username=sender_username)
        receiver = Peer.objects.get(username=receiver_username)

        msg = Message.objects.create(
            sender=sender,
            receiver=receiver,
            content=content
        )

        return JsonResponse(
            {
                "status": "ok",
                "message_id": msg.id
            },
            status=201
        )

    except Peer.DoesNotExist:
        return JsonResponse(
            {"error": "Sender or receiver not found"},
            status=404
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=500
        )

@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    try:
        data = json.loads(request.body)

        username = data.get("username")
        ip = data.get("ip")
        port = data.get("port")

        if not all([username, ip, port]):
            return JsonResponse(
                {"error": "username, ip and port are required"},
                status=400
            )

        peer, created = Peer.objects.update_or_create(
            username=username,
            defaults={
                "ip": ip,
                "port": port
            }
        )

        return JsonResponse(
            {
                "message": "Peer registered successfully",
                "created": created
            },
            status=201 if created else 200
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

@require_http_methods(["GET"])
def peers(request):
    peers = Peer.objects.all()

    data = [
        {
            "username": p.username,
        }
        for p in peers
    ]

    return JsonResponse(
        {"peers": data},
        status=200
    )

@require_http_methods(["GET"])
def peerinfo(request):
    username = request.GET.get("username")

    if not username:
        return JsonResponse(
            {"error": "username parameter is required"},
            status=400
        )

    try:
        peer = Peer.objects.get(username=username)
    except Peer.DoesNotExist:
        return JsonResponse(
            {"error": "Peer not found"},
            status=404
        )

    return JsonResponse(
        {
            "username": peer.username,
            "ip": peer.ip,
            "port": peer.port
        },
        status=200
    )

@csrf_exempt
@require_http_methods(["POST"])
def start_friendship(request):
    data = json.loads(request.body)

    username1 = data.get("user1")
    username2 = data.get("user2")

    peer1 = Peer.objects.get(username=username1)
    peer2 = Peer.objects.get(username=username2)

    friendship1 = Friendship.objects.create(owner=peer1, friend_username=peer2.username)

    return JsonResponse(
        {
            "message": "friendship started successfully",
        },
        status=200
    )

@csrf_exempt
@require_http_methods(["GET"])
def get_friends(request):
    username = request.GET.get("username")
    peer = Peer.objects.get(username=username)
    user_friends = Friendship.objects.filter(owner=peer)

    data = [
        {
            "username": friend.friend_username,
        }
        for friend in user_friends
    ]

    return JsonResponse(
        {
            "friends": data,
        },
        status=200
    )

@csrf_exempt
@require_http_methods(["GET"])
def get_messages(request):
    username1 = request.GET.get("peer1")
    username2 = request.GET.get("peer2")

    peer1 = Peer.objects.get(username=username1)
    peer2 = Peer.objects.get(username=username2)

    messages1 = Message.objects.filter(sender=peer1, receiver=peer2)
    messages2 = Message.objects.filter(sender=peer2, receiver=peer1)
    all_messages = messages1.union(messages2).order_by("timestamp")

    data = [
        {
            "message": message.content,
            "from": message.sender.username
        }
        for message in all_messages
    ]
    
    return JsonResponse(
        {
            "messages": data,
        },
        status=200
    )
