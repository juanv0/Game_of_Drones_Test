from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, get_user_model
from .func import first_wins
import json
from .forms import PlayerNameForm, PlayerRoundForm
from django.contrib.auth.decorators import login_required
from random import randint


"""
This is a clase based view aproach with session handling
"""
class Register(View):
    form_class = UserCreationForm
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        title = "Enter User Information"
        return render(request, 'registration.html',
            {'form':form, 'title':title})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password= password)
            login(request, user)
            return redirect('/startgame')
        else:
            return redirect("/register")

class StartGame(View):
    
    user = get_user_model()
    
    @login_required
    def get(self, request, *args, **kwargs):
        title = 'Single Game'
        return render(request, 'start_game_single.html',
                {'title': title})
                
    def post(self, request, *args, **kwargs):
        
        request.session['round'] = 0
        request.session["info"] = ""
        request.session["player_wins"] = 0
        request.session["comm_wins"] = 0
        return redirect("/playroundsolo")
        
        
        
class StartGame_old(View):

    form_class = PlayerNameForm
    user = get_user_model()
    @login_required
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        title = "Enter Player's Name"
        return render(request, "start_game_view.html",
                      {'form': form, 'title': title})

    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            request.session['player_1_name'] = form.cleaned_data["player_1_name"]
            request.session['player_2_name'] = form.cleaned_data["player_2_name"]
            request.session["info"] = ""
            request.session['round'] = 0
            request.session['round_real'] = 0
            request.session["player_1_wins"] = 0
            request.session["player_2_wins"] = 0
            return redirect("/playround")

        return render(request, "start_game_view.html", {'form': form})

class PlayRoundSolo(View):
    user = get_user_model()
    form_class = PlayerRoundForm
    @login_required
    def get(self, request, *args, **kwargs):

        form = self.form_class()
        list_matches = []
        list_rounds = []
        title = "Ronda " + str(request.session.get('round'))        
        if request.session.get("info"):
            matches = request.session.get("info").split("-")

            for match in matches:
                if match != "":
                    rounds, match = match.split(',')
                    list_rounds.append(rounds)
                    list_matches.append(match)

        return render(request, "play_round_solo.html",
                      {'form': form, 'title': title
                          , 'player': request.user.get_username(), 'rounds': list_rounds, 'matches': list_matches})

    @login_required
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        player_name = request.user.get_username()
        if form.is_valid():
            player_choice = [int(x) for x in form.cleaned_data["player_move"].replace('[','').replace(']','').split(',')];
            values= [[1,0,0],[0,1,0],[0,0,1]]
            comm_move = values[randint(0,2)]
            result = first_wins(player_choice, comm_move)
            
            if result > 0:
                request.session["player_wins"] += 1
                request.session["info"] +=\
                    str(request.session.get('round')) + "," + player_name + "-"
            elif result < 0:
                request.session["comm_wins"] += 1
                request.session["info"] +=\
                    str(request.session.get('round')) + "," + "Comm" + "-"
            else:
                request.session["info"] +=\
                    str(request.session.get('round')) + ", Draw -"
            request.session['round'] += 1                
            if request.session.get('player_wins') == 3:
                request.session["winner"] = player_name
                return redirect("/winnerview")
            elif request.session.get('comm_wins') == 3:
                request.session["winner"] = "Comm"
                return redirect("/winnerview")
            return redirect("/playroundsolo")
        return redirect("/playroundsolo")


class PlayRound(View):

    form_class = PlayerRoundForm
    def get(self, request, *args, **kwargs):

        form = self.form_class()
        list_matches = []
        list_rounds = []
        title = "Ronda " + str(request.session.get('round_real'))
        if request.session.get('player_1_name') and request.session.get('player_2_name'):
            if request.session.get("info"):
                matches = request.session.get("info").split("-")

                for match in matches:
                    if match != "":
                        rounds, match = match.split(',')
                        list_rounds.append(rounds)
                        list_matches.append(match)

            if request.session.get('round') % 2 == 0:
                name = request.session.get('player_1_name')

                return render(request, "play_round_view.html",
                              {'form': form, 'title': title
                                  , 'player': name, 'rounds': list_rounds, 'matches': list_matches})
            else:
                request.session['round_real'] += 1
                name = request.session.get('player_2_name')
                return render(request, "play_round_view.html",
                              {'form': form, 'title': title
                                  , 'player': name, 'rounds': list_rounds, 'matches': list_matches})

        return redirect("/startgame")

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            if request.session.get('round') % 2 == 0:
                request.session["player_1_move"] = form.cleaned_data['player_move']
            else:
                player_1_move = request.session.get("player_1_move")[1:-1].split(',')
                player_2_move = form.cleaned_data["player_move"]
                request.session["player_2_move"] = player_2_move
                player_2_move = player_2_move[1:-1].split(',')
                first_move = [int(n) for n in player_1_move]
                last_move = [int(n) for n in player_2_move]
                result = first_wins(first_move, last_move)
                if result > 0:
                    request.session["player_1_wins"] += 1
                    request.session["info"] +=\
                        str(request.session.get('round_real')) + "," + request.session.get('player_1_name') + "-"
                elif result < 0:
                    request.session["player_2_wins"] += 1
                    request.session["info"] +=\
                        str(request.session.get('round_real')) + "," + request.session.get('player_2_name') + "-"
                else:
                    request.session["info"] +=\
                        str(request.session.get('round_real')) + ", Draw -"
            request.session['round'] += 1
                
            if request.session.get('player_1_wins') == 3:
                request.session["winner"] = request.session.get('player_1_name')
                return redirect("/winnerview")
            elif request.session.get('player_2_wins') == 3:
                request.session["winner"] = request.session.get('player_2_name')
                return redirect("/winnerview")
            return redirect("/playround")
        return redirect("/playround")


class WinnerView(View):

    def get(self, request, *args, **kwargs):

        if request.session.get('winner'):
            title = "We have a WINNER!!"
            
            n = request.session.get('winner')
            message = "[" + n + "] is the new EMPEROR!"
            # to_write = request.session['player_1_name'] + ',' + \
                       # request.session['player_2_name'] + ',' + \
                       # str(request.session['round_real']) + ',' +\
                       # request.session['info'] + ',' + n
            # with open('data.txt','w') as file:
                # file.write(to_write)
                
            return render(request, "winner_view.html",
                          {'title': title, 'message': message})
        return redirect("/startgame")
