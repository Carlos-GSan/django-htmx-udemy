from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('delete-book/<int:pk>', views.delete_book, name='delete-book'),
]
