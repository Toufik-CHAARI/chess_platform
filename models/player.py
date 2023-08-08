from datetime import datetime


class Player:
    def __init__(
        self,
        first_name,
        last_name,
        birth_date,
        chess_id,
        ranking=None,
        score=0,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        if not isinstance(birth_date, datetime):
            raise ValueError("start_date must be a datetime object")
        self.chess_id = chess_id
        self.ranking = ranking
        self.score = score

    @staticmethod
    def from_dict(source):
        """
        This static method creates a new Player object from
        a dictionary source.The dictionary should contain
        the necessary information for initializing a Player
        object, including the first name, last name, birth date,
        chess ID,ranking, and score. The method converts the
        birth date from a string to a Python datetime object
        using the strptime method. It then creates a new
        Player object,sets its attributes accordingly,
        and returns it.
        """
        player = Player(
            source["first_name"],
            source["last_name"],
            datetime.strptime(source["birth_date"], "%d%m%Y"),
            source["chess_id"],
            source["ranking"],
            source["score"],
        )
        return player

    def to_dict(self):
        """
        This method converts the current Player object into a
        dictionary representation.It includes attributes
        such as the first name, last name, birth date
        (formatted as a string), chess ID, ranking,
        and score. The method returns a dictionary
        containing these attributes.
        """
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": self.birth_date.strftime("%d%m%Y"),
            "chess_id": self.chess_id,
            "ranking": self.ranking,
            "score": self.score,
        }
