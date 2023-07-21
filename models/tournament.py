import uuid
from datetime import datetime
from models.round import Round
from models.match import Match
from models.player import Player

class Tournament:
    def __init__(self, tournament_id, name, location, start_date, end_date, description, num_rounds=4, current_round=0, players=None, rounds=None):
    #def __init__(self, tournament_id, name, location, start_date, end_date,description, num_rounds=4, current_round=0, players=[], rounds=[]):
        self.tournament_id = tournament_id if tournament_id else str(uuid.uuid4())
        self.name = name
        self.location = location
        self.start_date = start_date
        if not isinstance(start_date, datetime):
            raise ValueError("start_date must be a datetime object")
        self.end_date = end_date
        if not isinstance(end_date, datetime):
            raise ValueError("end_date must be a datetime object")
        self.description = description
        self.num_rounds = num_rounds        
        self.current_round = current_round
        self.players = players if players else []
        #self.rounds = [round_.to_dict() for round_ in rounds] if rounds else []
        #self.players = players 
        self.rounds = rounds if rounds else []
    
    def add_round(self, round_name):
        new_round = Round(round_name)
        self.rounds.append(new_round)
        self.current_round += 1

    def add_match_to_round(self, round_name, match):
        for round_ in self.rounds:
            if round_.name == round_name:
                round_.matches.append(match)
                break 
            
            
    def get_round(self, round_name):
        for round in self.rounds:
            if round.name == round_name:
                return round
        return None
         
   
   # def to_dict(self):
       #return self.__dict__
    
    
    def to_dict(self):
        return {
            'tournament_id': self.tournament_id,
            'name': self.name,
            'location': self.location,
            'start_date': self.start_date.strftime('%d%m%Y'),
            'end_date': self.end_date.strftime('%d%m%Y'),
            'description': self.description,
            'current_round': self.current_round, 
            'rounds': [
                {
                    'name': round.name,
                    'matches': [match.to_dict() for match in round.matches],
                    'start_time': round.start_time.strftime('%d-%m-%Y %H:%M:%S') if round.start_time else None,
                    'end_time': round.end_time.strftime('%d-%m-%Y %H:%M:%S') if round.end_time else None,
                } for round in self.rounds],
            'players': [player.to_dict() for player in self.players],
            'num_rounds': self.num_rounds
        }



    @staticmethod
    def from_dict(source):
        tournament = Tournament(
            source["tournament_id"], 
            source["name"], 
            source["location"], 
            #source["start_date"],
            datetime.strptime(source["start_date"], '%d%m%Y'),
            datetime.strptime(source["end_date"], '%d%m%Y'), 
            #source["end_date"], 
            source["description"], 
            source.get("num_rounds",4),
            source.get("current_round",0),
            [Player.from_dict(player) for player in source["players"]],
            [Round.from_dict(round_) for round_ in source["rounds"]]
        )
        return tournament
        
    
   
        
