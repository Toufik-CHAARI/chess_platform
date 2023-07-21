from datetime import datetime


class Player:
    def __init__(self, first_name, last_name, birth_date, chess_id,ranking=None, score=0):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        if not isinstance(birth_date, datetime):
            raise ValueError("start_date must be a datetime object")
        self.chess_id = chess_id
        self.ranking = ranking
        self.score = score

    #convert to a dictionnary
    def to_dict(self):
        return self.__dict__
    
    '''
    #convert to an object
    @staticmethod
    def from_dict(source):
        return Player(**source)'''

    @staticmethod
    def from_dict(source):
        player = Player(
            source["first_name"], 
            source["last_name"], 
            datetime.strptime(source["birth_date"], '%d%m%Y'),
            source["chess_id"], 
            source["ranking"], 
            source["score"]
        )
        return player

    #convert to a dictionnary
    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": self.birth_date.strftime('%d%m%Y'),
            "chess_id":self.chess_id,
            "ranking":self.ranking,
            "score":self.score,
                
    
            }

