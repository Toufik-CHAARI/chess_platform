from datetime import datetime
from models.match import Match

class Round:
    def __init__(self, name,start_time=None, end_time=None):
        self.name = name
        self.start_time = start_time if start_time else datetime.now() 
        self.end_time = end_time
        self.matches = []  # list of Match objects

   

    def add_match(self, match):
        self.matches.append(match)
        
    def get_match(self, match_id):
        for match in self.matches:
            if match.match_id == match_id:       
                return match
        return None

    def end_round(self):
        self.end_time = datetime.now()
    
    
    def to_dict(self):
        return {
            'name': self.name,
            'start_time': self.start_time.strftime('%d-%m-%Y %H:%M:%S') if self.start_time else None,
            'end_time': self.end_time.strftime('%d-%m-%Y %H:%M:%S') if self.end_time else None,
            'matches': [match.to_dict() for match in self.matches]
        }
    
    @staticmethod
    def from_dict(source):
        print(source)
        round_obj = Round(source["name"])
        round_obj.start_time = datetime.strptime(source["start_time"], '%d-%m-%Y %H:%M:%S') if source["start_time"] else None
        round_obj.end_time = datetime.strptime(source["end_time"], '%d-%m-%Y %H:%M:%S') if source["end_time"] else None
        round_obj.matches = [Match.from_dict(match) for match in source["matches"]]
        return round_obj
    
    