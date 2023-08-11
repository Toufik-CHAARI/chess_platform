import json
from models.tournament import Tournament
from datetime import datetime
from models.match import Match
from controllers.players_controller import PlayerController
import uuid
import random


class TournamentController:
    def __init__(self):
        self.tournaments = []
        self.load_tournaments()
        self.players_to_match = []
        self.player_controller = PlayerController()

    def create_tournament(
        self,
        tournament_id,
        name,
        location,
        start_date,
        end_date,
        description,
        num_rounds,
        current_round=0,
        rounds=None,
        past_pairs=None,
    ):

        tournament = Tournament(
            tournament_id,
            name,
            location,
            start_date,
            end_date,
            description,
            num_rounds,
            current_round,
            rounds=[],
        )
        self.tournaments.append(tournament)
        self.save_tournaments()
        print("Tournoi créé avec succès!")

    def tournament_menu(self):
        """
        This function displays the tournament menu options.
        This function doesn't take any arguments and doesn't
        return anything.
        """
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

    def add_tournament_wrapper(self):
        """
        Wrapper function for adding a tournament.
        This function guides the user through the process of adding
        a new tournament.This function doesn't take any arguments
        and doesn't return anything.
        """
        tournament_id = input(
            "Identifiant du tournoi(généré automatiquement si vide): "
        )
        name = self.get_non_empty_input(
            "Nom du tournoi: ",
            "Vous devez fournir un nom de tournoi",
        )
        location = self.get_non_empty_input(
            "Lieu du tournoi: ",
            "Vous devez renseigner le lieu du tournoi",
        )
        start_date = self.get_date("Date de début (JJ-MM-AAAA): ")
        end_date = self.get_date("Date de fin (JJ-MM-AAAA): ")
        description = input("Description: ")
        num_rounds = input(
            "Nombre de rounds (par défaut 4 si champs vide): "
        )
        if num_rounds == "":
            num_rounds = 4
        else:
            num_rounds = int(num_rounds)
        self.create_tournament(
            tournament_id,
            name,
            location,
            start_date,
            end_date,
            description,
            num_rounds,
        )

    def tournament_list_wrapper(self):
        """
        Wrapper function for displaying a tournament as well as
        rounds and matches.This function doesn't take any
        arguments and doesn't return anything.
        """
        for tournament in self.tournaments:
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
                    print("------------------------------------")
                    print(f"Nom du Tour: {round.name}")
                    print(
                        "Date et heure de début :",
                        round.start_time,
                    )
                    print("Date et heure de fin :", round.end_time)
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

    def update_tournament_wrapper(self):
        """
        Wrapper function for updating a tournament.
        This function guides the user through the process
        of updating a new tournament.This function doesn't
        take any arguments and doesn't return anything.
        """
        tournament_id = input(
            "Renseigner l'identifiant du tournoi "
            "pour modifier un tournoi: "
        )
        name = input(" Nom du Tournoi (Meme nom si champs vide): ")
        location = input(
            " Localisation du Tournoi "
            "(Meme localisation si champs vide): "
        )
        start_date = self.get_date("Date de début (JJ-MM-AAAA): ")
        end_date = self.get_date("Date de fin (JJ-MM-AAAA): ")
        description = input("Description (mem description si vide): ")
        num_rounds = input(
            "Nombre de rounds (par défaut 4 si champs vide): "
        )
        if num_rounds == "":
            num_rounds = 4
        else:
            num_rounds = int(num_rounds)

        self.update_tournament(
            tournament_id,
            name,
            location,
            start_date,
            end_date,
            num_rounds,
            description,
        )

    def delete_tournament_wrapper(self):
        """
        Wrapper function for deleting a tournament.
        This function guides the user through the process
        of deleting an existing tournament.This function doesn't
        take any arguments and doesn't return anything.
        """
        tournament_id = self.get_non_empty_input(
            "Renseigner l'identifiant du tournoi à supprimer: ",
            "Vous devez impérativement fournir un identifiant",
        )
        self.delete_tournament(tournament_id)

    def start_round_wrapper(self):
        """
        Wrapper function for starting a new round.
        This function guides the user through the process
        of starting a new round.This function doesn't
        take any arguments and doesn't return anything.
        """
        tournament_id = self.get_non_empty_input(
            "Identifiant du tournoi: ",
            "Vous devez imperativement fournir l'identifiant "
            "du tournoi",
        )
        self.start_round(tournament_id)

    def end_round_wrapper(self):
        """
        Wrapper function for ending an existing round.
        This function guides the user through the process
        of ending an existing round.This function doesn't
        take any arguments and doesn't return anything.
        """
        tournament_id = self.get_non_empty_input(
            "Fournir l'identifiant du tournoi pour mettre "
            "fin au tour: ",
            "Vous devez imperativement fournir l'identifiant "
            "du tournoi",
        )
        round_name = self.get_non_empty_input(
            "Nom du tour:  ",
            "Vous devez imperativement renseigner le nom du tour",
        )
        self.end_round(tournament_id, round_name)

    def add_match_to_round_wrapper(self):
        """
        Wrapper function for manually adding a match to a round.
        This function guides the user through the process
        of manually adding a match to an existing round.This
        function doesn't take any arguments and doesn't return anything.
        """

        tournament_id = self.get_non_empty_input(
            "Identifiant du tournoi: ",
            "Vous devez imperativement fournir "
            "l'identifiant du tournoi",
        )
        match_id = input(
            "Identifiant du match (généré automatiquement si vide): "
        )
        round_name = self.get_non_empty_input(
            "Nom du tour:  ",
            "Vous devez imperativement renseigner le nom du tour",
        )

        player_one = self.player_controller.get_chess_id(
            "Identification National d échecs - Joueur 1: "
        )
        player_two = self.player_controller.get_chess_id(
            "Identification National d échecs - Joueur 2: "
        )
        score1 = self.get_score("Score - Joueur 1 : ")
        score2 = self.get_score("Score - Joueur 2: ")
        while score1 + score2 > 1:
            print("la somme des deux scores ne peut exceder 1")
            score1 = self.get_score("Score - Joueur 1 : ")
            score2 = self.get_score("Score - Joueur 2: ")
        self.add_match_to_round(
            tournament_id,
            match_id,
            round_name,
            player_one,
            player_two,
            score1,
            score2,
        )

    def automatic_match_wrapper(self):
        """
        Wrapper function for automatically adding a match to a round.
        This function guides the user through the process
        of automatically adding a match to an existing round.This
        function doesn't take any arguments and doesn't return anything.
        """
        tournament_id = self.get_non_empty_input(
            "Identifiant du tournoi: ",
            "Vous devez imperativement fournir "
            "l'identifiant du tournoi",
        )
        round_name = self.get_non_empty_input(
            "Nom du tour:  ",
            "Vous devez imperativement renseigner le nom du tour",
        )
        self.generate_match_automatic(tournament_id, round_name)

    def update_match_wrapper(self):
        """
        Wrapper function for updating a match.
        This function guides the user through the process
        of updating a match.This function doesn't take any
        arguments and doesn't return anything.
        """
        tournament_id = self.get_non_empty_input(
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
        score1 = self.get_score("Score - Joueur 1 : ")
        score2 = self.get_score("Score - Joueur 2: ")
        while score1 + score2 > 1:
            print("la somme des deux scores ne peut exceder 1")
            score1 = self.get_score("Score - Joueur 1 : ")
            score2 = self.get_score("Score - Joueur 2: ")
        self.update_match(
            tournament_id,
            match_id,
            player_one,
            player_two,
            score1,
            score2,
        )
        self.update_scores_after_match(
            tournament_id, match_id, score1, score2
        )

    def report_menu(self):
        """
        This function displays the report menu options.
        This function doesn't take any arguments and doesn't
        return anything.
        """
        print("------------------------------------")
        print("\nMenu des rapports:")
        print("1. Liste des Joueurs")
        print("2. Liste des Tournois")
        print("3. Détail tournoi")
        print("4. Revenir au menu principal")

    def short_tournament_list_wrapper(self):
        """
        Wrapper function for displaying tournament name and
        tournament id.This function doesn't take any arguments
        and doesn't return anything.
        """
        for tournament in self.tournaments:
            print("------------------------------------")
            print("Nom du Tournoi: ", tournament.name)
            print(
                "Identifiant du Tournoi: ",
                tournament.tournament_id,
            )
            print("------------------------------------")

    def tournament_details_wrapper(self):
        """
        Wrapper function for displaying all the attributes of
        tournaments including rounds and matches details .
        This function doesn't take any arguments and
        doesn't return anything.
        """
        tournament_id = input("Identifiant du Tournoi: ")
        self.display_tournament_details(tournament_id)

    def get_tournament(self, tournament_id):
        """
        Retrieve a given tournament by using its ID.
        It returns the Tournament object if found otherwise
        it return None.
        """
        for tournament in self.tournaments:
            if tournament.tournament_id == tournament_id:
                return tournament
        print("Tournoi inconnu!")
        return None

    def update_tournament(
        self,
        tournament_id,
        name=None,
        location=None,
        start_date=None,
        end_date=None,
        num_rounds=None,
        description=None,
    ):
        """
        This function updates the details of a specific tournament.
        The current value is kept if the new value is None.
        """
        tournament = self.get_tournament(tournament_id)
        if tournament:
            if name is not None:
                tournament.name = name
            if location is not None:
                tournament.location = location
            if start_date is not None:
                tournament.start_date = start_date
            if end_date is not None:
                tournament.end_date = end_date
            if num_rounds is not None:
                tournament.num_rounds = num_rounds
            if description is not None:
                tournament.description = description

            self.save_tournaments()
            print("Tournoi modifié avec succès !")
        else:
            print("Identifiant du Tournoi érroné")

    def delete_tournament(self, tournament_id):
        """
        this function deletes a specific tournament
        from the list of tournaments based on its ID.
        """
        tournament = self.get_tournament(tournament_id)
        if tournament:
            self.tournaments.remove(tournament)
            self.save_tournaments()
            print("Tournoi supprimé avec succes")
        else:
            print("Identifiant du tournoi érroné")

    def load_tournaments(self):
        """
        This function loads the tournament data from a JSON file.
        If there is an issue when decoding the JSON data, an error
        message is printed and the tournaments list is set to an
        empty list.
        """
        try:
            with open("data/tournaments.json", "r") as file:
                tournaments_data = json.load(file)
                self.tournaments = [
                    Tournament.from_dict(tournament)
                    for tournament in tournaments_data
                ]
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            self.tournaments = []

    def start_round(self, tournament_id):
        """
        This function starts a new round for a given tournament only if
        the current number of rounds is less than the maximum number of
        rounds allowed for the tournament.
        """
        tournament = self.get_tournament(tournament_id)
        if tournament:
            if tournament.current_round >= tournament.num_rounds:
                print(
                    "Impossible de créér un nouveau tour, vous avez "
                    "atteint le maximum de tour pour ce tournoi."
                )
            else:
                round_name = f"ROUND {tournament.current_round + 1}"
                tournament.add_round(round_name)
                self.save_tournaments()
                print("Nouveau Tour créé avec succès!")

    def add_match_to_round(
        self,
        tournament_id,
        match_id,
        round_name,
        player_one,
        player_two,
        score1,
        score2,
    ):
        """
        This function adds a match to a specific round
        of a specific tournament. It also updates the
        players' scores and ranks.
        Important !!! variable player_one and player_two
        contains chess_id
        """
        tournament = self.get_tournament(tournament_id)
        if not tournament:
            print(
                f"Aucun Tournoi ne correspond à l'identifiant: {tournament_id}"
            )
            return
        if not self.round_exists(tournament, round_name):
            print(
                "ce nom de tour n'existe pas, saisir en "
                "majuscule le nom du tour"
            )
            return

        match_id = match_id if match_id else str(uuid.uuid4())
        match = Match(match_id, player_one, player_two, score1, score2)

        match.set_scores(score1, score2)
        tournament.add_match_to_round(round_name, match)
        player_controller = PlayerController()
        player_controller.update_player_score_by_chess_id(
            player_one, score1
        )
        player_controller.update_player_score_by_chess_id(
            player_two, score2
        )
        player_controller.rank_players()
        self.save_tournaments()
        print("Résultat du match enregistré avec succes")

    def update_match(
        self,
        tournament_id,
        match_id,
        player_one=None,
        player_two=None,
        score1=None,
        score2=None,
    ):
        """
        This function updates a match within a specific tournament.
        Only the provided parameters will be updated. If a parameter
        is not provided, the corresponding match attribute will remain
        the same.
        """
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

    def round_exists(self, tournament, round_name):
        """
        This function checks if a round with the given name exists
        in the provided tournament.It returns True if a round with
        the specified name exists in the tournament otherwise it
        returns False.
        """
        return any(
            round.name == round_name for round in tournament.rounds
        )

    def end_round(self, tournament_id, round_name):
        """
        Ends a specific round in the given tournament by
        setting its end time to the current date and time.
        A success message is displayed if the round is successfully
        ended, or an error message if the round or tournament is not found.
        """
        tournament = self.get_tournament(tournament_id)
        if not tournament:
            print("Identifiant du Tournoi érroné")
            return

        if not self.round_exists(tournament, round_name):
            print(
                "ce nom de tour n'existe pas, saisir "
                "en majuscule le nom du tour"
            )
            return

        for round_ in tournament.rounds:
            if round_.name == round_name:
                round_.end_time = datetime.now()
                self.save_tournaments()
                print(f"Le Tour {round_name} est terminé!")
                return

    def save_tournaments(self):
        """
        This function saves the current list of tournaments
        to a JSON file.Each tournament is converted to a
        dictionary before it is saved.
        """
        with open("data/tournaments.json", "w") as file:
            json.dump(
                [
                    tournament.to_dict()
                    for tournament in self.tournaments
                ],
                file,
            )

    def update_players_to_match(self, tournament):
        """
        Update the players to be matched in a tournament.
        The players are sorted based on their scores in descending
        order, however players with same scores are sorted randomly.
        """
        current_scores = tournament.get_current_scores()
        controller = PlayerController()
        controller.load_players()

        self.players_to_match = sorted(
            controller.players,
            key=lambda player: (
                current_scores.get(player.chess_id, 0),
                random.random(),
            ),
            reverse=True,
        )

    def generate_match_automatic(self, tournament_id, round_name):
        """
        Generates a match between two players automatically in a
        specified round of the given tournament.In the first round,
        players are chosen randomly. In subsequent rounds,
        players with the highest scores who haven't played
        together yet are matched.A success message if the
        match could be generated, an error message if the
        tournament is not found, or a failure message if
        a valid player_two could not be found.
        """
        tournament = self.get_tournament(tournament_id)
        if not tournament:
            print(
                f"Aucun Tournoi ne correspond à "
                f"l'identifiant: {tournament_id}"
            )
            return

        if not self.round_exists(tournament, round_name):
            print(
                "ce nom de tour n'existe pas, saisir en "
                "majuscule le nom du tour"
            )
            return

        player_one = None
        player_two = None
        if tournament.current_round == 1:
            self.update_players_to_match(tournament)
            player_one, player_two = random.sample(
                self.players_to_match, 2
            )
            self.players_to_match.remove(player_one)
            self.players_to_match.remove(player_two)
            tournament.past_pairs.add(
                (player_one.chess_id, player_two.chess_id)
            )
        else:
            if not self.players_to_match:
                self.update_players_to_match(tournament)
            player_one = self.players_to_match.pop(0)
            for potential_player_two in self.players_to_match[
                :
            ]:  # Use a copy of the list
                if (
                    player_one.chess_id,
                    potential_player_two.chess_id,
                ) not in tournament.past_pairs and (
                    potential_player_two.chess_id,
                    player_one.chess_id,
                ) not in tournament.past_pairs:
                    tournament.past_pairs.add(
                        (
                            player_one.chess_id,
                            potential_player_two.chess_id,
                        )
                    )
                    self.players_to_match.remove(
                        potential_player_two
                    )  # Use remove() method instead of pop()
                    player_two = potential_player_two
                    break
            if not player_two:
                return "Unable to find a valid player_two"

        match_id = str(uuid.uuid4())
        match = Match(
            match_id, player_one.chess_id, player_two.chess_id, 0, 0
        )
        tournament.add_match_to_round(round_name, match)
        self.save_tournaments()
        print(
            "Génération de la paire de joueur effectuée avec succès !!!"
        )

    def display_tournament_details(self, tournament_id):
        """
        Display the details of a tournament based on its identifier.
        The details include the name and dates of the tournament,
        a list of players in alphabetical order,and a list of all
        rounds with their respective matches.
        """
        tournament = self.get_tournament(tournament_id)
        if not tournament:
            print("Aucun tournoi ne correspond à cet identifiant.")
            return

        print("Nom du tournoi:", tournament.name)
        print(
            "Dates du tournoi: Du",
            tournament.start_date,
            "au",
            tournament.end_date,
        )

        players_controller = PlayerController()
        players_controller.load_players()

        tournament_players_ids = {
            match.player1
            for round in tournament.rounds
            for match in round.matches
        }
        tournament_players_ids.update(
            {
                match.player2
                for round in tournament.rounds
                for match in round.matches
            }
        )

        tournament_players = [
            player
            for player in players_controller.players
            if player.chess_id in tournament_players_ids
        ]

        tournament_players.sort(
            key=lambda player: (player.last_name, player.first_name)
        )

        print("Liste des Joueurs:")
        for player in tournament_players:
            print(
                "-",
                player.last_name,
                player.first_name,
                player.chess_id,
            )

        print("Tours:")
        for round in tournament.rounds:
            print(round.name)
            for match in round.matches:

                player1 = players_controller.get_player(match.player1)
                player2 = players_controller.get_player(match.player2)

                if not player1 or not player2:
                    print(
                        f"Les joueurs {match.player1} et/ou "
                        f"{match.player2} n'existent pas."
                    )
                    continue
                print(
                    f"  Match: {player1.first_name} {player1.last_name} "
                    f"(ID: {player1.chess_id}) contre {player2.first_name} "
                    f"{player2.last_name} (ID: {player2.chess_id}),"
                    f"Score: {match.score1} - {match.score2}"
                )

    def update_scores_after_match(
        self, tournament_id, match_id, score1, score2
    ):
        """
        This function updates the scores of both players after
        each match.This function retrieves the tournament and
        match based on their IDs, updates the player scores,
        ranks the players, and saves the tournaments.
        A success message is displayed if the scores
        are updated successfully, or an error message
        if the match or tournament IDs are invalid.
        """
        tournament = self.get_tournament(tournament_id)
        if tournament:
            # Get the match across all rounds
            for round_ in tournament.rounds:
                match = round_.get_match(match_id)
                if match:
                    player_controller = PlayerController()
                    # update the players' scores
                    player_controller.update_player_score_by_chess_id(
                        match.player1, score1
                    )
                    player_controller.update_player_score_by_chess_id(
                        match.player2, score2
                    )
                    player_controller.rank_players()
                    self.save_tournaments()
                    print("Scores enregistrés avec succès!")
                    return
            print("Identifiant de match érronné!")
        else:
            print("Tournoi inconnu!")

    def get_score(self, prompt):
        """
        This function takes a prompt as input and allows the user
        to input a score value. It ensures that the input is a valid
        score for a match (1 = won, 0 = lost, or 0.5 = drawn) by
        using the PlayerController to validate the score.
        The user is asked to re-enter the value in case
        of invalid input or an empty input.
        """
        while True:
            player_controller = PlayerController()
            score_str = input(prompt).replace(",", ".")
            if score_str.strip() == "":
                print(
                    "Erreur de saisie !!! - Vous ne pouvez pas laisser "
                    "le champ vide."
                )
                continue
            try:
                score = float(score_str)
                if not player_controller.valid_score(score):
                    print(
                        "Erreur de saisie !!! - les résultats d'un "
                        "match sont  1 = gagné,0= perdu et 0.5 "
                    )
                    continue
                return score
            except ValueError:
                print(
                    "Erreur de saisie !!! - Veuillez entrer un nombre."
                )

    def get_date(self, prompt):
        """
        this function takes a prompt as input and allows the user
        to input a date in the format "DDMMYYYY". It converts
        the input string into a Python datetime object. If the user
        provides an invalid date format, he is asked to re-enter
        in the correct format.
        """
        while True:
            date_str = input(prompt)
            try:
                date_obj = datetime.strptime(date_str, "%d-%m-%Y")
                return date_obj
            except ValueError:
                print(
                    "Vous devez renseigner la date de la façon "
                    "suivante: JOUR MOIS ANNEE (avec traits d'union) "
                )

    def get_non_empty_input(self, prompt, error_message):
        """
        This function takes a prompt and an error message as inputs.
        It allows the user to input some text and ensures that the
        input is not empty (whitespace-only). If the input is empty,
        it displays the provided error message and prompts the user
        to re-enter a non-empty input.
        """
        result = input(prompt)
        while result.strip() == "":
            print(error_message)
            result = input(prompt)
        return result
