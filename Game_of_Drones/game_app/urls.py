from django.shortcuts import redirect
from django.views.generic import RedirectView
from .views import StartGame, PlayRound, WinnerView, Register, StartGame_old, PlayRoundSolo
from django.urls import path, re_path
from django.contrib.auth import views

urlpatterns = [
    path("startgame_old/", StartGame_old.as_view(), name="Start Game"),
    path('startgame/', StartGame.as_view(), name='Start Game'),
    #re_path(r'^.*$', RedirectView.as_view(url='startgame/', permanent=False), name='Start Game'),
    #path('', lambda request: redirect('startgame/', permanent=False)),
    path("playround/", PlayRound.as_view(), name="Play Round"),
    path('playroundsolo/', PlayRoundSolo.as_view(), name='Play Round'),
    path("winnerview/", WinnerView.as_view(), name="Winner"),
    path("", StartGame.as_view(), name="Start Game"),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password-change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('register/', Register.as_view(), name='register'),
]
