from models.player import Player
import json
import os
import re

class PlayerController:
    
    def __init__(self):
        self.players = []
        self.load_players()
        
    def add_player(self, first_name, last_name, birth_date, chess_id, ranking=None, score=0):
        
        player = Player(first_name, last_name, birth_date, chess_id, ranking, score)
        self.players.append(player)
        self.save_players()
        print(f"le nouveau joueur '{player.first_name}' a été enregistré")
    
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
            if chess_id:                
                player.chess_id = chess_id                  
            if first_name:
                player.first_name = first_name
            if last_name:
                player.last_name = last_name
            if birth_date:
                player.birth_date = birth_date
            self.save_players()
            print( 'Modifications des données joueur enregistrées')
        else:
            print( "L'identifiant fournie ne correspond pas !!!")

    def delete_player(self, chess_id):
        player = self.get_player(chess_id)
        if player:
            self.players.remove(player)
            self.save_players()
            print( 'Suppression joueur effectuée avec succcès')
        else:
            print( "L'identifiant fournie ne correspond pas !!!")   
    
            
    def load_players(self):
            try:
                with open("data/players.json", "r") as file:
                    player_list = json.load(file)
                    self.players = [Player.from_dict(player) for player in player_list]                   
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
        
    def valid_score(self,score):
        if score in [0, 0.5, 1]:
            return True
        else:
            return False


    def valid_score_int(self, score):
        try:
            # Try to convert the input to an integer
            float(score)
            return True
        except ValueError:
            # If a ValueError is raised, the input is not an integer
            return False
        
    def list_players_alphabetically(self):
        sorted_players = sorted(self.players, key=lambda player: player.first_name)
        for player in sorted_players:
            print(f'Chess ID: {player.chess_id}, Prénom: {player.first_name},Nom: {player.last_name}, Score: {player.score}')