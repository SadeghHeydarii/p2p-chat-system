from django.contrib import admin
from .models import Peer

@admin.register(Peer)
class PeerAdmin(admin.ModelAdmin):
    list_display = ('username', 'ip', 'port', 'last_seen')
