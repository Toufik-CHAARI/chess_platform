import uuid


class Match:
    def __init__(self, match_id, player1, player2, score1, score2):
        self.match_id = match_id if match_id else str(uuid.uuid4())
        self.player1 = player1
        self.player2 = player2
        self.score1 = score1
        self.score2 = score2

    def __repr__(self):
        """
        Returns a string representation of the Match object.
        """
        return (
            f"Match(player1={self.player1},"
            f"player2={self.player2},"
            f" score1={self.score1},"
            f"score2={self.score2})"
        )

    def set_scores(self, score1, score2):
        """
        Set the scores for player 1 and player 2 in the match.
        Parameters:
        score1 : The score for player 1.
        score2 : The score for player 2.
        """
        self.score1 = score1
        self.score2 = score2

    @classmethod
    def from_dict(cls, source):
        """
        This class method (decorated with @classmethod) creates a new
        Match object from a dictionary source.The dictionary should
        contain the necessary information for initializing a Match
        object,including the match ID, names of player 1 and
        player 2, and their respective scores.The method uses
        the class cls (i.e., Match) to create a new Match
        object with the provided information and returns it.
        """
        print(source)
        match = Match(
            source["match_id"],
            source["player1"],
            source["player2"],
            source["score1"],
            source["score2"],
        )
        return match

    def to_dict(self):
        """
        This method converts the current Match object into a
        dictionary representation.It includes attributes
        such as the match ID, names of player 1 and player 2,
        and their respective scores. The method returns a
        dictionary containing these attributes.
        """
        return {
            "match_id": self.match_id,
            "player1": self.player1,
            "player2": self.player2,
            "score1": self.score1,
            "score2": self.score2,
        }
