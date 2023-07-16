from datetime import datetime
from models.match import Match

class Round:
    def __init__(self, name):
        self.name = name
        self.start_time="" 
        self.end_time =""
        self.matches = []  # list of Match objects

   

    def add_match(self, match):
        self.matches.append(match)
        
    def get_match(self, match_id):
        for match in self.matches:
            if match.id == match_id:  
                return match
        return None

    def end_round(self):
        self.end_time 
    
    
    def to_dict(self):
        return self.__dict__
    
    @staticmethod
    def from_dict(source):
        print(source)
        round_obj = Round(source["name"])
        round_obj.start_time = source["start_time"]
        round_obj.end_time = source["end_time"]
        round_obj.matches = [Match.from_dict(match) for match in source["matches"]]
        return round_obj
    
    '''def to_dict(self):
        return {
            'name': self.name,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'matches': [match.to_dict() for match in self.matches]  # assuming you also have to_dict in Match class
        }'''
        