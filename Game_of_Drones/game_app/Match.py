from .func import first_wins
from .Player import Player

"""
Match class will be created for every game passin two arguments of type Person
it will hold the information of every round played in a match, also will have 
a method tho know if there is a winner and who is the winner
"""


class Match:
    
    def __init__(self, p1, p2):
        
        self.p1 = p1
        self.p2 = p2
    
    def run_match(self, v1, v2):
        
        if first_wins(v1, v2):
            print("gano primero: "+self.p1.name)
            self.p1.roud_win()
        else:
            print("gano segundo: "+self.p2.name)  
            self.p2.roud_win()
    
    def has_winner(self):
    
        if self.p1.wins() or self.p2.wins():
            return True
        else:
            return False
            
    def who_wins(self):
        result = self.p1 if self.p1.wins else self.p2
        return result
