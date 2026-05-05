from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from core.models import Room

# Create your views here.
def index(request):
    context = {'rooms': Room.objects.all()}
    return render(request, 'index.html', context)

@login_required
def room(request, room_slug):
    room = get_object_or_404(Room, slug=room_slug)
    messages = room.messages.all()
    context = {'room': room,
               'messages': messages}
    return render(request, 'room.html', context)