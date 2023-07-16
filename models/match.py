import uuid


class Match:
    def __init__(self,match_id,  player1, player2, score1, score2):
        self.match_id= match_id if match_id else str(uuid.uuid4())
        #self.players = [player_one, player_two]
        #self.scores = [0, 0]  # initial score for both players is 0
        self.player1 = player1
        self.player2 = player2
        self.score1 = score1
        self.score2 = score2
    
    def __repr__(self):
        return f"Match(player1={self.player1}, player2={self.player2}, score1={self.score1}, score2={self.score2})"    
    
    def set_scores(self, score1, score2):
        self.scores = [score1, score2]
        
    #def to_dict(self):
       # return self.__dict__
    
    @classmethod
    def from_dict(cls, source):
        print(source)
        match = Match(
                source["match_id"],
                source["player1"],
                source["player2"],
                source["score1"],
                source["score2"]
            )
        return match
    
    
    def to_dict(self):
        return {
          "match_id":self.match_id,  
          "player1": self.player1,
          "player2": self.player2,
          "score1": self.score1,
          "score2": self.score2,
        }
        
        
