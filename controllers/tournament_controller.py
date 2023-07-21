import json
from models.tournament import Tournament
from models.player import Player
from datetime import datetime
from models.round import Round
from models.match import Match
from controllers.players_controller import PlayerController
import uuid
import os


class TournamentController:
    def __init__(self):
        self.tournaments = []        
        self.load_tournaments()

    def create_tournament(self, tournament_id, name, location, start_date, end_date,description, num_rounds, current_round=0, players=None, rounds=None):
                            
        tournament = Tournament(tournament_id, name, location, start_date, end_date,description, num_rounds, current_round, players=[], rounds=[])
        self.tournaments.append(tournament)
        self.save_tournaments()
        print("Tournament successfully created!")

    def list_tournaments(self):
        for tournament in self.tournaments:
            print(f'Tournament_id: {tournament.tournament_id}, Name: {tournament.name}, Location: {tournament.location}, Start Date: {tournament.start_date},End Date: {tournament.end_date},Descrition: {tournament.description}, Number of Rounds: {tournament.num_rounds}, Current Round:{tournament.current_round}')

    
        
    def get_tournament(self, tournament_id):
        for tournament in self.tournaments:
            if tournament.tournament_id == tournament_id:
                return tournament
        print("Tournament not found!")
        return None

    def update_tournament(self, tournament_id):
        tournament = self.get_tournament(tournament_id)
        if tournament:
            tournament.name = input("Saisir le nom du Tournoi (appuyer sur entrer pour conserver le nom actuel): ") or tournament.name
            tournament.location = input("Saisir la nouvelle localisation du Tournoi (appuyer sur entrer pour conserver la localisation actuelle): ") or tournament.location
            tournament.start_date = input("Saisir la nouvelle date de début (appuyer sur entrer pour conserver la date début actuelle): ") or tournament.start_date
            tournament.end_date = input("Saisir la nouvelle date de fin (appuyer sur entrer pour conserver la date de fin actuelle): ") or tournament.end_date
            tournament.num_rounds = input("Saisir le nouveau nombre de Tours(appuyer sur entrer pour conserver le nombre actuel): ") or tournament.num_rounds
            tournament.description = input("Saisir une nouvelle description (appuyer sur entrer pour conserver la description actuelle): ") or tournament.description
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
                self.tournaments = [Tournament.from_dict(tournament) for tournament in tournaments_data]
                #self.tournaments = [Tournament(**data) for data in tournaments_data]
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            self.tournaments = []
        
    def start_round(self, tournament_id, round_name):
        tournament = self.get_tournament(tournament_id)
        if tournament:
            if tournament.current_round >= tournament.num_rounds:
                print("Impossible de créér un nouveau tour, vous avez atteint le maximum de tour pour ce tournoi.")
            else:
                tournament.add_round(round_name)
                self.save_tournaments()
                print("Nouveau Tour créé avec succès!")
        '''if tournament:
            tournament.add_round(round_name)
            self.save_tournaments()
            print("Round successfully created!")'''
   
    def add_match_to_round(self,tournament_id,match_id, round_name, player_one, player_two,score1, score2):
        tournament = self.get_tournament(tournament_id)
        if tournament:
            match_id= match_id if match_id else str(uuid.uuid4())
            match = Match(match_id, player_one, player_two, score1, score2)
            #variable player_one and two contains chess_id
            match.set_scores(score1,score2)
            tournament.add_match_to_round(round_name, match)            
            player_controller = PlayerController()
            # update the players' scores
            player_controller.update_player_score_by_chess_id(player_one, score1)
            player_controller.update_player_score_by_chess_id(player_two, score2)
            player_controller.rank_players()    
            self.save_tournaments()
            
    
    def update_match(self, tournament_id, match_id, player_one=None, player_two=None, score1=None, score2=None):
        tournament = self.get_tournament(tournament_id)
        if tournament:
            # Find the match across all rounds
            for round_ in tournament.rounds:
                match = round_.get_match(match_id)
                if match:
                    match.player1 = player_one or match.player1
                    match.player2 = player_two or match.player2
                    if score1 is not None:
                        match.score1 = score1
                    if score2 is not None:
                        match.score2 = score2

                    self.save_tournaments()
                    print("Match modifié avec succès!")
                    return
            print("cet identifiant ne correspond à aucun match!")
        else:
            print("Tournoi introuvable!")

            
    def end_round(self, tournament_id):
        tournament = self.get_tournament(tournament_id)
        if tournament:
            current_round = tournament.rounds[tournament.current_round - 1]
            current_round.end_time = datetime.now()
            self.save_tournaments()
            print(f"Le Tour {tournament.current_round} est terminé!")
            
    
               
            
            

    def save_tournaments(self):
        with open('data/tournaments.json', 'w') as file:
            json.dump([tournament.to_dict() for tournament in self.tournaments], file)
            
'''
class PlayerController:
    def __init__(self):
        self.players = []
        self.load_players()
        
    def load_players(self):
            if os.path.isfile("data/players.json"):
                with open("data/players.json", "r") as file:
                    player_list = json.load(file)
                    for player_dict in player_list:
                        player = Player(**player_dict)
                        self.players.append(player)
                        
    def save_players(self):
            player_list = [player.to_dict() for player in self.players]
            with open("data/players.json", "w") as file:
                json.dump(player_list, file)

    def update_player_score(self, player_id, new_score):
            # Find the player
            player = self.get_player(player_id)
            if player:
                # Update the player's score
                player.score += new_score  # Assuming 'score' attribute exists in Player

                self.save_players()  # Save players data to file
                
                
'''