class Player():
    
    def __init__(self, name):
        self.name = name
        self.total_wins = 0
    
    def round_win(self):
        self.total_wins += 1
        
    def wins(self):
        return True if self.total_wins == 3 else False
