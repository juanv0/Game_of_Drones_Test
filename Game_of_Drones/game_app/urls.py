from django.shortcuts import redirect
from django.views.generic import RedirectView
from .views import StartGame, PlayRound, WinnerView
from django.urls import path, re_path

urlpatterns = [
    path("startgame/", StartGame.as_view(), name="Start Game"),
    #re_path(r'^.*$', RedirectView.as_view(url='startgame/', permanent=False), name='Start Game'),
    #path('', lambda request: redirect('startgame/', permanent=False)),
    path("playround/", PlayRound.as_view(), name="Play Round"),
    path("winnerview/", WinnerView.as_view(), name="Winner"),
]
