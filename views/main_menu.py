class MainMenu:
    def __init__(self, player_controller, tournament_controller):
        self.player_controller = player_controller
        self.tournament_controller = tournament_controller

    def display(self):
        while True:
            print("\n Menu Principal:")
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
                self.report_menu()
            elif choice == "4":
                break
            else:
                print("Option invalide")

    def player_menu(self):
        while True:
            print("------------------------------------")
            print("\nMenu Joueur:")
            print("1. Ajouter un joueur")
            print("2. Mettre à jour un joueur")
            print("3. Supprimer un joueur")
            print("4. Lister les joueurs")
            print("5. Quitter")
            choice = input("Choisissez une option: ")

            if choice == "1":
                first_name = self.player_controller.get_non_empty_input(
                    "Prénom: ",
                    "Vous devez impérativement fournir prénom !!!",
                )
                last_name = self.player_controller.get_non_empty_input(
                    "Nom: ",
                    "Vous devez impérativement fournir un nom de famille !!!",
                )
                birth_date = self.tournament_controller.get_date(
                    "Date de naissance (JJ-MM-AAAA): "
                )
                chess_id = self.player_controller.validate_chess_id(
                    "Identifiant national d’échecs: "
                )
                self.player_controller.add_player(
                    first_name, last_name, birth_date, chess_id
                )
                break

            elif choice == "2":
                chess_id = self.player_controller.get_chess_id(
                    "Identification National d échecs : "
                )
                first_name = input(
                    "Nouveau prénom (laissez vide pour ne pas changer): "
                )
                last_name = input(
                    "Nouveau nom de famille (laissez vide "
                    "pour ne pas changer): "
                )
                birth_date = self.tournament_controller.get_date(
                    "Nouvelle Date de naissance (JJ-MM-AAAA): "
                )
                self.player_controller.update_player(
                    chess_id, first_name, last_name, birth_date
                )
                break

            elif choice == "3":
                chess_id = self.player_controller.get_chess_id(
                    "Identification National d échecs - Joueur 2: "
                )
                self.player_controller.delete_player(chess_id)
                break

            elif choice == "4":
                for player in self.player_controller.players:
                    print("------------------------------------")
                    print(
                        "Identifiant National d'échecs: ",
                        player.chess_id,
                    )
                    print("Prénom: ", player.first_name)
                    print("Nom: ", player.last_name)
                    print(
                        "Date de naissance: ",
                        player.birth_date.strftime("%d-%m-%Y"),
                    )
                    print("Score: ", player.score)
                    print("Ranking: ", player.ranking)
                    print("------------------------------------")

            elif choice == "5":
                break
            else:
                print("Option invalide.")

    def tournament_menu(self):
        while True:
            print("------------------------------------")
            print("\nMenu des tournois:")
            print("1. Créer un tournoi")
            print("2. Afficher les tournois")
            print("3. Modifier un tournoi")
            print("4. Supprimer un tournoi")
            print("5. Démarrez un tour dans un tournoi")
            print("6. Finir un tour en cours")
            print("7. Ajout manuel d'un match au tour d'un tournoi")
            print("8. Generation automatique de match")
            print("9. Modifier / Enregistrer le resultat d'un match")
            print("10. Revenir au menu principal")
            choice = input("Choisissez une option: ")

            if choice == "1":
                tournament_id = input(
                    "Identifiant du tournoi(généré automatiquement si vide): "
                )
                name = self.tournament_controller.get_non_empty_input(
                    "Nom du tournoi: ",
                    "Vous devez fournir un nom de tournoi",
                )
                location = (
                    self.tournament_controller.get_non_empty_input(
                        "Lieu du tournoi: ",
                        "Vous devez renseigner le lieu du tournoi",
                    )
                )
                start_date = self.tournament_controller.get_date(
                    "Date de début (JJ-MM-AAAA): "
                )
                end_date = self.tournament_controller.get_date(
                    "Date de fin (JJ-MM-AAAA): "
                )
                description = input("Description: ")
                num_rounds = input(
                    "Nombre de rounds (par défaut 4 si champs vide): "
                )
                if num_rounds == "":
                    num_rounds = 4
                else:
                    num_rounds = int(num_rounds)
                self.tournament_controller.create_tournament(
                    tournament_id,
                    name,
                    location,
                    start_date,
                    end_date,
                    description,
                    num_rounds,
                )

            elif choice == "2":
                for (
                    tournament
                ) in self.tournament_controller.tournaments:
                    # print(tournament.__dict__)
                    print("------------------------------------")
                    print("Nom du Tournoi: ", tournament.name)
                    print(
                        "Identifiant du Tournoi: ",
                        tournament.tournament_id,
                    )
                    print("Lieu du Tournoi: ", tournament.location)
                    print(
                        "Date de début: ",
                        tournament.start_date.strftime("%d-%m-%Y"),
                    )
                    print(
                        "Date de fin: ",
                        tournament.end_date.strftime("%d-%m-%Y"),
                    )
                    print("Description: ", tournament.description)
                    print("Nombre de Tour: ", tournament.num_rounds)
                    print("Tour actuel: ", tournament.current_round)
                    if tournament.rounds:
                        for round in tournament.rounds:
                            print(
                                "------------------------------------"
                            )
                            print(f"Nom du Tour: {round.name}")
                            print(
                                "Date et heure de début :",
                                round.start_time,
                            )
                            print(
                                "Date et heure de fin :", round.end_time
                            )
                            print("Matches:")
                            for match in round.matches:
                                print(
                                    "Identifiant du match :",
                                    match.match_id,
                                )
                                print(
                                    "Identifiant Joueur 1 :",
                                    match.player1,
                                )
                                print(
                                    "Identifiant Joueur 2 :",
                                    match.player2,
                                )
                                print("Score Joueur-1 :", match.score1)
                                print("Score Joueur-2 :", match.score2)

                    print("------------------------------------")

            elif choice == "3":
                tournament_id = input(
                    "Renseigner l'identifiant du tournoi "
                    "pour modifier un tournoi: "
                )
                name = input(
                    " Nom du Tournoi (Meme nom si champs vide): "
                )
                location = input(
                    " Localisation du Tournoi "
                    "(Meme localisation si champs vide): "
                )
                start_date = self.tournament_controller.get_date(
                    "Date de début (JJ-MM-AAAA): "
                )
                end_date = self.tournament_controller.get_date(
                    "Date de fin (JJ-MM-AAAA): "
                )
                description = input(
                    "Description (mem description si vide): "
                )
                num_rounds = input(
                    "Nombre de rounds (par défaut 4 si champs vide): "
                )
                if num_rounds == "":
                    num_rounds = 4
                else:
                    num_rounds = int(num_rounds)

                self.tournament_controller.update_tournament(
                    tournament_id,
                    name,
                    location,
                    start_date,
                    end_date,
                    num_rounds,
                    description,
                )

            elif choice == "4":

                tournament_id = self.tournament_controller.get_non_empty_input(
                    "Renseigner l'identifiant du tournoi à supprimer: ",
                    "Vous devez impérativement fournir un identifiant",
                )
                self.tournament_controller.delete_tournament(
                    tournament_id
                )

            elif choice == "5":
                tournament_id = self.tournament_controller.get_non_empty_input(
                    "Identifiant du tournoi: ",
                    "Vous devez imperativement fournir l'identifiant "
                    "du tournoi",
                )
                self.tournament_controller.start_round(tournament_id)

            elif choice == "6":
                tournament_id = self.tournament_controller.get_non_empty_input(
                    "Fournir l'identifiant du tournoi pour mettre "
                    "fin au tour: ",
                    "Vous devez imperativement fournir l'identifiant "
                    "du tournoi",
                )
                round_name = self.tournament_controller.get_non_empty_input(
                    "Nom du tour:  ",
                    "Vous devez imperativement renseigner le nom du tour",
                )
                self.tournament_controller.end_round(
                    tournament_id, round_name
                )

            elif choice == "7":
                tournament_id = (
                    self.tournament_controller.get_non_empty_input(
                        "Identifiant du tournoi: ",
                        "Vous devez imperativement fournir "
                        "l'identifiant du tournoi",
                    )
                )
                match_id = input(
                    "Identifiant du match (généré automatiquement si vide): "
                )
                round_name = self.tournament_controller.get_non_empty_input(
                    "Nom du tour:  ",
                    "Vous devez imperativement renseigner le nom du tour",
                )
                player_one = self.player_controller.get_chess_id(
                    "Identification National d échecs - Joueur 1: "
                )
                player_two = self.player_controller.get_chess_id(
                    "Identification National d échecs - Joueur 2: "
                )
                score1 = self.tournament_controller.get_score(
                    "Score - Joueur 1 : "
                )
                score2 = self.tournament_controller.get_score(
                    "Score - Joueur 2: "
                )
                while score1 + score2 > 1:
                    print("la somme des deux scores ne peut exceder 1")
                    score1 = self.tournament_controller.get_score(
                        "Score - Joueur 1 : "
                    )
                    score2 = self.tournament_controller.get_score(
                        "Score - Joueur 2: "
                    )
                self.tournament_controller.add_match_to_round(
                    tournament_id,
                    match_id,
                    round_name,
                    player_one,
                    player_two,
                    score1,
                    score2,
                )

            elif choice == "8":

                tournament_id = (
                    self.tournament_controller.get_non_empty_input(
                        "Identifiant du tournoi: ",
                        "Vous devez imperativement fournir "
                        "l'identifiant du tournoi",
                    )
                )
                round_name = self.tournament_controller.get_non_empty_input(
                    "Nom du tour:  ",
                    "Vous devez imperativement renseigner le nom du tour",
                )
                self.tournament_controller.generate_match_automatic(
                    tournament_id, round_name
                )

            elif choice == "9":
                tournament_id = self.tournament_controller.get_non_empty_input(
                    "Identifiant du tournoi: ",
                    "Vous devez imperativement fournir l'identifiant "
                    "du tournoi",
                )
                match_id = input("Identifiant du match : ")
                player_one = self.player_controller.get_chess_id(
                    "Identification National d échecs - Joueur 1: "
                )
                player_two = self.player_controller.get_chess_id(
                    "Identification National d échecs - Joueur 2: "
                )
                score1 = self.tournament_controller.get_score(
                    "Score - Joueur 1 : "
                )
                score2 = self.tournament_controller.get_score(
                    "Score - Joueur 2: "
                )
                while score1 + score2 > 1:
                    print("la somme des deux scores ne peut exceder 1")
                    score1 = self.tournament_controller.get_score(
                        "Score - Joueur 1 : "
                    )
                    score2 = self.tournament_controller.get_score(
                        "Score - Joueur 2: "
                    )
                self.tournament_controller.update_match(
                    tournament_id,
                    match_id,
                    player_one,
                    player_two,
                    score1,
                    score2,
                )
                self.tournament_controller.update_scores_after_match(
                    tournament_id, match_id, score1, score2
                )
                break

            elif choice == "10":
                break
            else:
                print("Option invalide")

    def report_menu(self):
        while True:
            print("------------------------------------")
            print("\nMenu des rapports:")
            print("1. Liste des Joueurs")
            print("2. Liste des Tournois")
            print("3. Détail tournoi")
            print("4. Quitter")
            choice = input("Choisissez une option: ")

            if choice == "1":
                self.player_controller.list_players_alphabetically()
            elif choice == "2":
                for (
                    tournament
                ) in self.tournament_controller.tournaments:
                    # print(tournament.__dict__)
                    print("------------------------------------")
                    print("Nom du Tournoi: ", tournament.name)
                    print(
                        "Identifiant du Tournoi: ",
                        tournament.tournament_id,
                    )
                    print("------------------------------------")
            elif choice == "3":
                tournament_id = input("Identifiant du Tournoi: ")
                self.tournament_controller.display_tournament_details(
                    tournament_id
                )
            elif choice == "4":
                break
            else:
                print("Option invalide.")
