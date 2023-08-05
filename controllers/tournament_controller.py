import json
from models.tournament import Tournament
from models.player import Player
from datetime import datetime
from models.round import Round

from models.match import Match
from controllers.players_controller import PlayerController
import uuid
import os
import random


class TournamentController:
    def __init__(self):
        self.tournaments = []        
        self.load_tournaments()
        self.players_to_match = []

    def create_tournament(self, tournament_id, name, location, start_date, end_date,description, num_rounds, current_round=0,rounds=None,past_pairs=None ):
                            
        tournament = Tournament(tournament_id, name, location, start_date, end_date,description, num_rounds, current_round,rounds=[])
        self.tournaments.append(tournament)
        self.save_tournaments()
        print("Tournoi créé avec succès!")

    def list_tournaments(self):
        for tournament in self.tournaments:
            print(f'Tournament_id: {tournament.tournament_id}, Name: {tournament.name}, Location: {tournament.location}, Start Date: {tournament.start_date},End Date: {tournament.end_date},Descrition: {tournament.description}, Number of Rounds: {tournament.num_rounds}, Current Round:{tournament.current_round}')

    
        
    def get_tournament(self, tournament_id):
        for tournament in self.tournaments:
            if tournament.tournament_id == tournament_id:
                return tournament
        print("Tournoi inconnu!")
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
            print("Tournoi modifié avec succès !")

    def delete_tournament(self, tournament_id):
        tournament = self.get_tournament(tournament_id)
        if tournament:
            self.tournaments.remove(tournament)
            self.save_tournaments()
            print("Tournoi supprimé avec succes")

    def load_tournaments(self):
        try:
            with open('data/tournaments.json', 'r') as file:
                tournaments_data = json.load(file)
                self.tournaments = [Tournament.from_dict(tournament) for tournament in tournaments_data]            
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            self.tournaments = []
        
    def start_round(self, tournament_id):
        tournament = self.get_tournament(tournament_id)
        if tournament:
            if tournament.current_round >= tournament.num_rounds:
                print("Impossible de créér un nouveau tour, vous avez atteint le maximum de tour pour ce tournoi.")
            else:
                round_name = f"ROUND {tournament.current_round + 1}"
                tournament.add_round(round_name)
                self.save_tournaments()
                print("Nouveau Tour créé avec succès!")
        
   
    def add_match_to_round(self,tournament_id,match_id, round_name, player_one, player_two,score1, score2):
        tournament = self.get_tournament(tournament_id)
        if tournament:
            match_id = match_id if match_id else str(uuid.uuid4())
            match = Match(match_id, player_one, player_two, score1, score2)
            #Important !!! variable player_one and player_two contains chess_id
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
        else:
            print('Identifiant du Tournoi érroné')            
    
    def save_tournaments(self):
        with open('data/tournaments.json', 'w') as file:
            json.dump([tournament.to_dict() for tournament in self.tournaments], file)
            
    
    
    #v2
    def update_players_to_match(self,tournament):
        current_scores = tournament.get_current_scores()        
        controller = PlayerController()
        controller.load_players()       
        #self.players_to_match = sorted(controller.players, key=lambda player: current_scores.get(player.chess_id, 0), reverse=True)
        
        # Here we use random.random() as a second sorting key, so that players with the same score are sorted randomly.
        self.players_to_match = sorted(controller.players, key=lambda player: (current_scores.get(player.chess_id, 0), random.random()), reverse=True)
        print(current_scores)
            
    def generate_random_match(self, tournament_id, round_name):
        tournament = self.get_tournament(tournament_id)
        if not tournament:
            return f"Aucun Tournoi ne correspond à l'identifiant: {tournament_id}"
        player_one = None
        player_two = None
        if tournament.current_round == 1:
            self.update_players_to_match(tournament)
            player_one, player_two = random.sample(self.players_to_match, 2)
            self.players_to_match.remove(player_one)  # Remove player_one from the list
            self.players_to_match.remove(player_two)  # Remove player_two from the list
            tournament.past_pairs.add((player_one.chess_id, player_two.chess_id))
            #self.update_players_to_match(tournament)
            #player_one, player_two = random.sample(self.players_to_match, 2)
            #tournament.past_pairs.add((player_one.chess_id, player_two.chess_id))
        else:
            if not self.players_to_match:
                self.update_players_to_match(tournament)
            player_one = self.players_to_match.pop(0)
            for potential_player_two in self.players_to_match[:]:  # Use a copy of the list to avoid problems
                if (player_one.chess_id, potential_player_two.chess_id) not in tournament.past_pairs and (potential_player_two.chess_id, player_one.chess_id) not in tournament.past_pairs:
                    tournament.past_pairs.add((player_one.chess_id, potential_player_two.chess_id))
                    self.players_to_match.remove(potential_player_two)  # Use remove() method instead of pop()
                    player_two = potential_player_two
                    break
            if not player_two:
                return "Unable to find a valid player_two"
        match_id = str(uuid.uuid4())
        match = Match(match_id, player_one.chess_id, player_two.chess_id, 0, 0)
        tournament.add_match_to_round(round_name, match)
        self.save_tournaments()
        return "Génération de la paire de joueur effectuée avec succès !!!"
        
              
    
    def display_tournament_details(self, tournament_id):
        # Get the tournament
        tournament = self.get_tournament(tournament_id)
        if not tournament:
            print("Aucun tournoi ne correspond à cet identifiant.")
            return

        # Display name and dates of the tournament
        print("Nom du tournoi:", tournament.name)
        print("Dates du tournoi: Du", tournament.start_date, "au", tournament.end_date)

        # Display the list of players in alphabetical order.
        players_controller = PlayerController()
        players_controller.load_players()

        # Get the list of the players who participate to the tournament.
        tournament_players_ids = {match.player1 for round in tournament.rounds for match in round.matches}
        tournament_players_ids.update({match.player2 for round in tournament.rounds for match in round.matches})
        
        tournament_players = [player for player in players_controller.players if player.chess_id in tournament_players_ids]
        # Sorted Alphabetically
        tournament_players.sort(key=lambda player: (player.last_name, player.first_name))

        print("Liste des Joueurs:")
        for player in tournament_players:
            print("-", player.last_name, player.first_name, player.chess_id)

        # Display the list of all the rounds and all the matches
        print("Tours:")
        for round in tournament.rounds:
            print(round.name)
            for match in round.matches:
                # Get the Player objects corresponding based player id's which are chess_id
                player1 = players_controller.get_player(match.player1)
                player2 = players_controller.get_player(match.player2)
                # Vérifier si les joueurs existent
                if not player1 or not player2:
                    print(f"Les joueurs {match.player1} et/ou {match.player2} n'existent pas.")
                    continue
                print(f"  Match: {player1.first_name} {player1.last_name} (ID: {player1.chess_id}) contre {player2.first_name} {player2.last_name} (ID: {player2.chess_id}), Score: {match.score1} - {match.score2}")

        
    
           
    


    def update_scores_after_match(self, tournament_id, match_id, score1, score2):
        tournament = self.get_tournament(tournament_id)
        if tournament:
            # Get the match across all rounds
            for round_ in tournament.rounds:
                match = round_.get_match(match_id)
                if match:
                    player_controller = PlayerController()
                    # update the players' scores
                    player_controller.update_player_score_by_chess_id(match.player1, score1)
                    player_controller.update_player_score_by_chess_id(match.player2, score2)
                    player_controller.rank_players()
                    self.save_tournaments()
                    print("Scores enregistrés avec succès!")
                    return
            print("Identifiant de match érronné!")
        else:
            print("Tournoi inconnu!")