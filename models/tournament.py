import uuid
from datetime import datetime
from models.round import Round


class Tournament:
    def __init__(
        self,
        tournament_id,
        name,
        location,
        start_date,
        end_date,
        description,
        num_rounds=4,
        current_round=0,
        rounds=None,
    ):

        self.tournament_id = (
            tournament_id if tournament_id else str(uuid.uuid4())
        )
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
        self.rounds = rounds if rounds else []
        self.past_pairs = set()

    def add_round(self, round_name):
        """
        This function takes a round_name as input and adds a new
        round to the tournament. It creates a new Round object with
        the provided round_name, appends it to the self.rounds list,
        and increments the self.current_round attribute to keep track
        of the current round number.
        """
        new_round = Round(round_name)
        self.rounds.append(new_round)
        self.current_round += 1

    def add_match_to_round(self, round_name, match):
        """
        This function takes a round_name and a match as inputs and
        adds the match to the specified round in the tournament.
        It searches for the round with the provided round_name in
        the self.rounds list and appends the match to its matches
        attribute.If the specified round is found, the function
        adds the match to it; otherwise, it does nothing.
        """
        for round_ in self.rounds:
            if round_.name == round_name:
                round_.matches.append(match)
                break

    def get_round(self, round_name):
        """
        This function takes a round_name as input and searches for
        the round with the provided round_name in the tournament.
        If a round with the matching round_name is found, the function
        returns the Round object representing that round; otherwise,
        it returns None.
        """
        for round in self.rounds:
            if round.name == round_name:
                return round
        return None

    def to_dict(self):
        """
        This function converts the tournament object into a
        dictionary.It gathers various attributes of the tournament,
        such as tournament ID, name,location, start date, end date,
        description, current round number,past pairs, and the
        rounds' details, and returns them as a dictionary.The
        rounds are represented as a list of dictionaries containing
        their name, matches, start time, and end time
        (formatted as strings). The matches are also converted
        into dictionaries using the to_dict() method of the Match
        class.
        """
        return {
            "tournament_id": self.tournament_id,
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date.strftime("%d%m%Y"),
            "end_date": self.end_date.strftime("%d%m%Y"),
            "description": self.description,
            "current_round": self.current_round,
            "past_pairs": [list(pair) for pair in self.past_pairs],
            "rounds": [
                {
                    "name": round.name,
                    "matches": [
                        match.to_dict() for match in round.matches
                    ],
                    "start_time": round.start_time.strftime(
                        "%d-%m-%Y %H:%M:%S"
                    )
                    if round.start_time
                    else None,
                    "end_time": round.end_time.strftime(
                        "%d-%m-%Y %H:%M:%S"
                    )
                    if round.end_time
                    else None,
                }
                for round in self.rounds
            ],
            "num_rounds": self.num_rounds,
        }

    @staticmethod
    def from_dict(source):
        """
         The described static method constructs a new Tournament
        object using the information from a dictionary.
        This dictionary should include details such as
        the tournament ID, name, location, start and end dates,
        description, number of rounds, current round number,
        past pairs, and round details. The method also converts
        the start and end dates from strings to Python datetime
        objects and initializes the past_pairs attribute if the
        key is present. The newly created Tournament object is
        then returned.
        """
        tournament = Tournament(
            source["tournament_id"],
            source["name"],
            source["location"],
            # source["start_date"],
            datetime.strptime(source["start_date"], "%d%m%Y"),
            datetime.strptime(source["end_date"], "%d%m%Y"),
            # source["end_date"],
            source["description"],
            source.get("num_rounds", 4),
            source.get("current_round", 0),
            # [Player.from_dict(player) for player in source["players"]],
            [Round.from_dict(round_) for round_ in source["rounds"]],
        )
        if "past_pairs" in source:
            tournament.past_pairs = {
                tuple(pair) for pair in source["past_pairs"]
            }
        return tournament

    def get_current_scores(self):
        """
        This method calculates the current scores of all players
        participating in the tournament.It iterates through each
        round in the self.rounds list and each match in each round.
        For each match, it updates the scores of both players in
        a dictionary named current_scores.The method returns
        current_scores, which contains the accumulated scores
        for each player up to the current round.
        """
        current_scores = {}
        for round_ in self.rounds:
            for match in round_.matches:
                current_scores[match.player1] = (
                    current_scores.get(match.player1, 0) + match.score1
                )
                current_scores[match.player2] = (
                    current_scores.get(match.player2, 0) + match.score2
                )
        return current_scores
