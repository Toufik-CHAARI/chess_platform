from models.player import Player
from models.match import Match
import json
import uuid
from datetime import datetime



class MainMenu:
    def __init__(self, player_controller, tournament_controller):
        self.player_controller = player_controller
        self.tournament_controller = tournament_controller
    
    
    def display(self):
        while True:
            print("\nMain Menu:")
            print("1. Gérer les joueurs")
            print("2. Gérer les tournois")
            print("3. Accéder aux rapports")
            print("4. Quitter")
            choice = input("Choisissez une option: ")

            if choice == "1":
                self.player_menu()
            elif choice == "2":
                self.tournament_menu()
            elif choice == "3":
                self.tournament_menu()           
            elif choice == "4":
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
                while first_name == "":
                    print('Vous devez impérativement fournir un prénom')
                    first_name = input("Prénom: ")                    
                last_name = input("Nom de famille: ")
                while last_name =="":
                    print('Vous devez impérativement fournir un prénom')
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
            print("5. Démarrez un tour dans un tournoi")
            print("6. Finir le tour en cours")
            print("7. Ajouter un match au tour d'un tournoi")            
            print("8. Revenir au menu principal")
            
            choice = input("Choisissez une option: ")

            if choice == "1":
                tournament_id= input("Identifiant du tournois(généré automatiquement si vide): ")
                name = input("Nom du tournoi: ")
                while name == '':
                    print('Vous devez fournir un nom de tournoi')
                    name = input("Nom du tournoi: ")
                location = input("Lieu du tournoi: ")
                while location == '':
                    print('Vous devez renseigner le lieu du tournoi')
                    location = input("Lieu du tournoi: ")
                #start_date = datetime.strptime(input("Date de début (JJ-MM-AAAA): "), "%d%m%Y")
                try:
                    start_date = datetime.strptime(input("Date de début (JJ-MM-AAAA): "), "%d%m%Y")
                except ValueError:
                    start_date = None
                while not start_date:
                    print("Vous devez renseigner la date de la façon suivante: JOUR-MOIS-ANNEE : ")
                    try:
                        start_date = datetime.strptime(input("Date de début (JJ-MM-AAAA): "), "%d%m%Y")
                    except ValueError:
                        start_date = None

                try:
                    end_date = datetime.strptime(input("Date de fin (JJ-MM-AAAA): "), "%d%m%Y")
                except ValueError:
                    end_date = None
                while not end_date:
                    print("Vous devez renseigner la date de la façon suivante: JOUR-MOIS-ANNEE : ")
                    try:
                        end_date = datetime.strptime(input("Date de fin (JJ-MM-AAAA): "), "%d%m%Y")
                    except ValueError:
                        start_date = None
               
                    
                #end_date = input("Date de fin (YYYY-MM-DD): ")
                description = input("Description: ")
                num_rounds = input("Nombre de rounds (par défaut 4 si champs vide): ")
                if num_rounds == '':
                    num_rounds= 4
                else:
                    num_rounds = int(num_rounds)                
                self.tournament_controller.create_tournament(tournament_id, name, location, start_date, end_date,description,num_rounds)
            elif choice == "2":
                #for tournament in self.tournament_controller.tournaments:
                    #print(tournament.__dict__,end="\n")
                #self.tournament_controller.list_tournaments()
                for tournament in self.tournament_controller.tournaments:
                    #print(tournament.__dict__)
                    print('Nom du Tournoi: ',tournament.name)
                    print('Identifiant du Tournoi: ',tournament.tournament_id)
                    print('Lieu du Tournoi: ',tournament.location)
                    print('Date de début: ',tournament.start_date.strftime("%d-%m-%Y"))
                    print('Date de fin: ',tournament.end_date.strftime("%d-%m-%Y"))
                    print('Description: ',tournament.description)
                    print('Nombre de Tour: ',tournament.num_rounds)
                    print('Tour actuel: ',tournament.current_round)
                    
                    if tournament.rounds:
                                  
                        for round in tournament.rounds:
                            print(f"Nom du Tour: {round.name}")
                            print(f"Matches:")
                            for match in round.matches:
                                print('Identifiant du match :',match.match_id)
                                print('Identifiant Joueur 1 :',match.player1)
                                print('Identifiant Joueur 2 :',match.player2)
                                print('Score Joueur-1 :',match.score1)
                                print('Score Joueur-2 :',match.score2) 
                    print('------------------------------------')
            elif choice == "3":
                tournament_id = input("Renseigner l'identifiant du tournoi pour modifier un tournoi: ")
                self.tournament_controller.update_tournament(tournament_id)
            elif choice == "4":
                tournament_id = input("Renseigner l'identifiant du tournoi à supprimer: ")
                self.tournament_controller.delete_tournament(tournament_id)            
                 
            elif choice == "5":
                tournament_id = input("Identifiant du tournoi: ")
                while tournament_id == "" :
                    print("Vous devez imperativement fournir l'identifiant du tournoi")
                    tournament_id = input("Identifiant du tournoi: ")
                    
                round_name = input("Nom du Tour: ")
                while round_name == "":
                    print('Vous devez fournir un nom pour chaque tour')
                    round_name = input("Nom du tour: ")
                self.tournament_controller.start_round(tournament_id, round_name)
            
            elif choice == "6":
                tournament_id = input("Fournir l'identifiant du tournoi pour mettre fin au tour: ")
                self.tournament_controller.end_round(tournament_id)
            
            elif choice == "7":
                tournament_id = input("Identifiant du tournoi: ")
                while tournament_id == '':
                    print('Vous devez renseigner obligatoirement l identifiant du tournoi !!!')
                    tournament_id = input("Identifiant du tournoi: ")
                match_id = input("Identifiant du match (généré automatiquement si vide): ")
                round_name = input("Renseigner le nom du tour:  ")
                while round_name =='':
                    print('Vous devez fournir un nom de tour')
                    round_name = input("Renseigner le nom du tour:  ")
                player_one = input("Identification National d échecs - Joueur 1: ")
                while player_one =='':
                    print('Vous devez fournir un Identification National d échecs')
                    player_one = input("Identification National d échecs - Joueur 1: ")
                player_two = input("Identification National d échecs - Joueur 2:  ")
                while player_two =='':
                    print('Vous devez fournir un Identification National d échecs')
                    player_two = input("Identification National d échecs - Joueur 2 ")
                score1 = int(input("Score - Joueur 1 : "))
                score2 = int(input("Score - Joueur 2: "))
                
                self.tournament_controller.add_match_to_round(tournament_id,match_id,round_name, player_one, player_two, score1, score2)
                
            elif choice == "8":
                break
            else:
                print("Option invalide")

