from models.player import Player
import json
import os

class PlayerController:
    def __init__(self):
        self.players = []
        self.load_players()
        
    def add_player(self, first_name, last_name, birth_date, chess_id, ranking=None, score=0):
        player = Player(first_name, last_name, birth_date, chess_id, ranking, score)
        self.players.append(player)
        self.save_players()

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
            if os.path.isfile("data/players.json"):
                with open("data/players.json", "r") as file:
                    player_list = json.load(file)
                    for player_dict in player_list:
                        player = Player(**player_dict)
                        self.players.append(player)
    
    def list_players(self):
        for player in self.players:
            print(f'Prénom: {player.first_name}, Nom de famille: {player.last_name}, Date de naissance: {player.birth_date}, ID échecs: {player.chess_id},Ranking: {player.ranking},Score: {player.score}')
