import uuid
from datetime import datetime

class Tournament:
    def __init__(self, tournament_id, name, location, start_date, end_date,description, num_rounds=4, current_round=0, players=[], rounds=[]):
        self.tournament_id = tournament_id if tournament_id else str(uuid.uuid4())
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.num_rounds = num_rounds        
        self.current_round = current_round
        self.players = players 
        self.rounds = rounds 
         
        
        
    def to_dict(self):
        return {
            "tournament_id": self.tournament_id,
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "current_round": self.current_round,
            "players":  self.players,  # assuming you have to_dict in Player class
            "rounds":  self.rounds,
            
        }
        
