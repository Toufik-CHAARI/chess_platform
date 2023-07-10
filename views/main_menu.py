from models.player import Player
import json


class MainMenu:
    def __init__(self, player_controller, tournament_controller):
        self.player_controller = player_controller
        self.tournament_controller = tournament_controller
    
    
    def display(self):
        while True:
            print("\nMain Menu:")
            print("1. Gérer les joueurs")
            print("2. Gérer les tournois")
            print("3. Quitter")
            choice = input("Choisissez une option: ")

            if choice == "1":
                self.player_menu()
            elif choice == "2":
                self.tournament_menu()
            elif choice == "3":
                break
            else:
                print("Option invalide")       
        
        
    def player_menu(self):    
        while True:
            print("\nMenu:")
            print("1. Ajouter un joueur")
            print("2. Mettre à jour un joueur")
            print("3. Supprimer un joueur")
            print("4. Lister les joueurs") # New option
            print("5. Quitter")
            choice = input("Choisissez une option: ")

            if choice == "1":
                first_name = input("Prénom: ")
                last_name = input("Nom de famille: ")
                birth_date = input("Date de naissance (YYYY-MM-DD): ")
                chess_id = input("Identifiant national d’échecs: ")
                ranking = input("Ranking: ")
                score = input("score: ")
                self.player_controller.add_player(first_name, last_name, birth_date, chess_id)
            elif choice == "2":
                chess_id = input("Identifiant national d’échecs: ")
                first_name = input("Nouveau prénom (laissez vide pour ne pas changer): ")
                last_name = input("Nouveau nom de famille (laissez vide pour ne pas changer): ")
                birth_date = input("Nouvelle date de naissance (laissez vide pour ne pas changer): ")
                ranking = input("Ranking: ")
                score = input("score: ")
                self.player_controller.update_player(chess_id, first_name, last_name, birth_date)
            elif choice == "3":
                chess_id = input("Identifiant national d’échecs: ")
                self.player_controller.delete_player(chess_id)
            elif choice == "4":
                self.player_controller.list_players()
            elif choice == "5":
                break
            else:
                print("Option invalide.")
                
    def tournament_menu(self):
        while True:
            print("\nMenu des tournois:")
            print("1. Créer un tournoi")
            print("2. Afficher les tournois")
            print("3. Modifier un tournoi")
            print("4. Supprimer un tournoi")
            print("5. Revenir au menu principal")
            
            choice = input("Choisissez une option: ")

            if choice == "1":
                tournament_id= input("Identifiant du tournois: ")
                name = input("Nom du tournoi: ")
                location = input("Lieu du tournoi: ")
                start_date = input("Date de début (YYYY-MM-DD): ")
                end_date = input("Date de fin (YYYY-MM-DD): ")
                description = input("Description: ")
                num_rounds = input("Nombre de rounds (par défaut 4): ")
                if num_rounds == '':
                    num_rounds= 4
                else:
                    num_rounds = int(num_rounds)
                
                self.tournament_controller.create_tournament(tournament_id, name, location, start_date, end_date,description,num_rounds)
            elif choice == "2":
                for tournament in self.tournament_controller.tournaments:
                    print(tournament.__dict__)
            elif choice == "3":
                tournament_id = input("Enter the tournament id to update: ")
                self.tournament_controller.update_tournament(tournament_id)
            elif choice == "4":
                tournament_id = input("Enter the tournament id to delete: ")
                self.tournament_controller.delete_tournament(tournament_id)            
            elif choice == "5":
                break
            else:
                print("Option invalide")

          
'''
filename = 'numbers.json'          #use the file extension .json
with open(filename, 'w') as file_object:  #open the file in write mode
    json.dump(PlayerEncoder().encode(x), file_object)
'''