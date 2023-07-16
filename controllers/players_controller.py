from models.player import Player
import json
import os
import re

class PlayerController:
    
    def __init__(self):
        self.players = []
        self.load_players()
        
    def add_player(self, first_name, last_name, birth_date, chess_id, ranking=None, score=0):
        
        while not self.validate_chess_id(chess_id):
            print("Identifiant invalide !!! Format 2 lettres en majuscule suivis de 5 chiffres(ex:AB12345).")
            chess_id = input("Identifiant national d’échecs: ")
        player = Player(first_name, last_name, birth_date, chess_id, ranking, score)
        self.players.append(player)
        self.save_players()
        print('le nouveau joueur a été enregistré')
    
    def validate_chess_id(self,chess_id):
    # This pattern checks for 2 uppercase letters followed by 5 digits
        pattern = re.compile(r'^[A-Z]{2}\d{5}$')
        return bool(pattern.match(chess_id))

    def save_players(self):
        player_list = [player.to_dict() for player in self.players]
        with open("data/players.json", "w") as file:
            json.dump(player_list, file)
        
       
    def get_player(self, chess_id):
        for player in self.players:
            if player.chess_id == chess_id:
                return player
            
        return None

    def update_player(self, chess_id, first_name=None, last_name=None, birth_date=None):
        player = self.get_player(chess_id)
        if player:
            if first_name:
                player.first_name = first_name
            if last_name:
                player.last_name = last_name
            if birth_date:
                player.birth_date = birth_date
        self.save_players()

    def delete_player(self, chess_id):
        player = self.get_player(chess_id)
        if player:
            self.players.remove(player)
        self.save_players()   
    
            
    def load_players(self):
            try:
                with open("data/players.json", "r") as file:
                    player_list = json.load(file)
                    self.players = [Player.from_dict(player) for player in player_list]
                   # for player_dict in player_list:
                        #player = Player(**player_dict)
                        #self.players.append(player)
            except (FileNotFoundError, json.JSONDecodeError):
                self.players = []
            
    def list_players(self):
        for player in self.players:
            print(f'Prénom: {player.first_name}, Nom de famille: {player.last_name}, Date de naissance: {player.birth_date}, ID échecs: {player.chess_id},Ranking: {player.ranking},Score: {player.score}')

    def update_player_score_by_chess_id(self, chess_id, new_score):
    # Find the player
        for player in self.players:
            if player.chess_id == chess_id:
                # Update the player's score
                player.score += new_score
                self.save_players()  # Save players data to file
                return
        print(f"Player with chess_id {chess_id} not found.")
        
    def rank_players(self):
        # Sort players in descending order by score
        sorted_players = sorted(self.players, key=lambda player: player.score, reverse=True)
        # Update each player's ranking based on their position in the sorted list
        for i, player in enumerate(sorted_players, start=1):
            player.ranking = i
        self.save_players()  # Save players data to file

