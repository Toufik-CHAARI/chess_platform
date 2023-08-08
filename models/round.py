from datetime import datetime
from models.match import Match


class Round:
    def __init__(self, name, start_time=None, end_time=None):
        self.name = name
        self.start_time = start_time if start_time else datetime.now()
        self.end_time = end_time
        self.matches = []

    def add_match(self, match):
        """
        This method adds a match to the matches list of the
        current round.
        It appends the provided match object to the list.
        """
        self.matches.append(match)

    def get_match(self, match_id):
        """
        This method searches for a match in the matches list
        with the provided match_id.If a match with the matching
        match_id is found, it returns the Match object
        representing that match; otherwise, it returns None.
        """
        for match in self.matches:
            if match.match_id == match_id:
                return match
        return None

    def end_round(self):
        """
        This method sets the end_time attribute of the current round
        to the current date and time,indicating the end time of the
        round. It uses datetime.now() to obtain the current date and
        time.
        """
        self.end_time = datetime.now()

    def to_dict(self):
        """
        This method converts the current round object into a dictionary
        representation.It includes attributes such as the round name,
        start time (formatted as a string if available, otherwise None),
        end time (formatted as a string if available, otherwise None),
        and the list of matches (where each match is represented as a
        dictionary using the to_dict() method of the Match class).
        """
        return {
            "name": self.name,
            "start_time": self.start_time.strftime("%d-%m-%Y %H:%M:%S")
            if self.start_time
            else None,
            "end_time": self.end_time.strftime("%d-%m-%Y %H:%M:%S")
            if self.end_time
            else None,
            "matches": [match.to_dict() for match in self.matches],
        }

    @staticmethod
    def from_dict(source):
        """
        This static method creates a new Round object from a
        dictionary source.The dictionary should contain the
        necessary information for initializing a Round object,
        including the round name, start time, end time, and
        details of matches. The method converts the start
        and end times from strings to Python datetime objects
        using the strptime method. It then creates a new Round
        object, sets its attributes accordingly, and returns it.
        """
        print(source)
        round_obj = Round(source["name"])
        round_obj.start_time = (
            datetime.strptime(source["start_time"], "%d-%m-%Y %H:%M:%S")
            if source["start_time"]
            else None
        )
        round_obj.end_time = (
            datetime.strptime(source["end_time"], "%d-%m-%Y %H:%M:%S")
            if source["end_time"]
            else None
        )
        round_obj.matches = [
            Match.from_dict(match) for match in source["matches"]
        ]
        return round_obj
