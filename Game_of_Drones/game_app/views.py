from django.shortcuts import render, redirect
from django.views.generic import View
from .func import first_wins
import json
from .forms import PlayerNameForm, PlayerRoundForm

"""
This is a clase based view aproach with session handling
"""


class StartGame(View):
    form_class = PlayerNameForm

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
            to_write = request.session['player_1_name'] + ',' + \
                       request.session['player_2_name'] + ',' + \
                       str(request.session['round_real']) + ',' +\
                       request.session['info'] + ',' + n
            with open('data.txt','w') as file:
                file.write(to_write)
                
            return render(request, "winner_view.html",
                          {'title': title, 'message': message})
        return redirect("/startgame")
