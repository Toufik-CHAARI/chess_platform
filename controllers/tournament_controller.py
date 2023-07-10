import json
from models.tournament import Tournament
from models.player import Player

from datetime import datetime


class TournamentController:
    def __init__(self):
        self.tournaments = []
        self.load_tournaments()

    def create_tournament(self, tournament_id, name, location, start_date, end_date,description, num_rounds, current_round=0, players=None, rounds=None):
                            
        tournament = Tournament(tournament_id, name, location, start_date, end_date,description, num_rounds, current_round, players=[], rounds=[])
        self.tournaments.append(tournament)
        self.save_tournaments()
        print("Tournament successfully created!")

    def get_tournament(self, tournament_id):
        for tournament in self.tournaments:
            if tournament.tournament_id == tournament_id:
                return tournament
        print("Tournament not found!")

    def update_tournament(self, tournament_id):
        tournament = self.get_tournament(tournament_id)
        if tournament:
            tournament.name = input("Enter new name (press enter to keep current): ") or tournament.name
            tournament.location = input("Enter new location (press enter to keep current): ") or tournament.location
            tournament.start_date = input("Enter new start date (press enter to keep current): ") or tournament.start_date
            tournament.end_date = input("Enter new end date (press enter to keep current): ") or tournament.end_date
            tournament.num_rounds = input("Enter new number of rounds (press enter to keep current): ") or tournament.rounds
            tournament.description = input("Enter new description (press enter to keep current): ") or tournament.description
            self.save_tournaments()
            print("Tournament successfully updated!")

    def delete_tournament(self, tournament_id):
        tournament = self.get_tournament(tournament_id)
        if tournament:
            self.tournaments.remove(tournament)
            self.save_tournaments()
            print("Tournament successfully deleted!")

    def load_tournaments(self):
        try:
            with open('data/tournaments.json', 'r') as file:
                tournaments_data = json.load(file)
                self.tournaments = [Tournament(**data) for data in tournaments_data]
        except FileNotFoundError:
            self.tournaments = []
                
            
            

    def save_tournaments(self):
        with open('data/tournaments.json', 'w') as file:
            json.dump([tournament.to_dict() for tournament in self.tournaments], file)
            

   