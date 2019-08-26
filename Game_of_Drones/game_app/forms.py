from django import forms


ACTION_LIST = [
    ([1,0,0], 'Scissors'),
    ([0,1,0], 'Paper'),
    ([0,0,1], 'Rock'),
]


class PlayerNameForm(forms.Form):

    player_1_name = forms.CharField(label="Player 1", max_length=100)
    player_2_name = forms.CharField(label="Player 2", max_length=100)


class PlayerRoundForm(forms.Form):

    player_move = forms.CharField(label='Select Move: ',
                                    widget=forms.Select(choices=ACTION_LIST))
