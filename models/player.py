


class Player:
    def __init__(self, first_name, last_name, birth_date, chess_id,ranking=None, score=0):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.chess_id = chess_id
        self.ranking = ranking
        self.score = score

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": self.birth_date,
            "chess_id":self.chess_id,
            "ranking":self.ranking,
            "score":self.score,
                
    
            }

