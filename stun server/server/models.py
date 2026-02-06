from django.db import models

class Peer(models.Model):
    username = models.CharField(max_length=50, unique=True)
    ip = models.GenericIPAddressField()
    port = models.PositiveIntegerField()
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

class Friendship(models.Model):
    owner = models.ForeignKey(
        Peer,
        on_delete=models.CASCADE,
        related_name="friends"
    )
    friend_username = models.CharField(max_length=50)
    
    
class Message(models.Model):
    sender = models.ForeignKey(
        Peer,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        Peer,
        on_delete=models.CASCADE,
        related_name="received_messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"
