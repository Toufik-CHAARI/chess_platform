from models.player import Player
import json
import re


class PlayerController:
    def __init__(self):
        self.players = []
        self.load_players()

    def add_player(
        self,
        first_name,
        last_name,
        birth_date,
        chess_id,
        ranking=None,
        score=0,
    ):
        """
        This function adds a new player .
        It creates a new Player object using the given first_name,
        last_name, birth_date, chess_id, ranking, and score.
        The player is then added to the list of players and the list
        is updated and saved. A message is printed when the new player
        has been successfully recorded.
        """
        player = Player(
            first_name, last_name, birth_date, chess_id, ranking, score
        )
        self.players.append(player)
        self.save_players()
        print(
            f"le nouveau joueur '{player.first_name}' a été enregistré"
        )

    def get_non_empty_input(self, prompt, error_message):
        """
        This function takes a prompt and an error message as inputs.
        It allows the user to input some text, and ensures that
        the input is not empty (whitespace-only). If the input is
        empty,the provided error message is displayed and
        the user is asked to re-enter a non-empty input.
        """
        result = input(prompt)
        while result.strip() == "":
            print(error_message)
            result = input(prompt)
        return result

    def validate_chess_id(self, prompt):
        """
        This function takes a prompt as input and prompts the user to
        input a chess ID.It then checks that the input complies with the
        provided regular expression pattern to ensure that the chess ID
        is in the correct format: two uppercase letters followed by five
        digits. If the input is empty or does not match the pattern,
        error messages are displayed, and the user is asked
        to re-enter the chess ID until it matches the required format.
        """
        pattern = re.compile(r"^[A-Z]{2}\d{5}$")
        chess_id = input(prompt)
        while not chess_id.strip() or not pattern.match(chess_id):
            if not chess_id.strip():
                print("Vous ne pouvez pas laisser le champ vide.")
            else:
                print(
                    "Format incorrect! L'ID d'échecs doit être composé "
                    "de 2 lettres majuscules suivies de 5 chiffres."
                )
            chess_id = input(prompt)
        return chess_id

    def save_players(self):
        """
        This function saves the list of players into a JSON file.
        It converts each player in the player list into a dictionary
        using the to_dict() method and creates a list of these
        dictionaries.
        """
        player_list = [player.to_dict() for player in self.players]
        with open("data/players.json", "w") as file:
            json.dump(player_list, file)

    def get_player(self, chess_id):
        """
        This function searches for a player in the player list
        based on chess_id argument. If a player with the
        matching chess ID is found, the function returns that player
        object; otherwise, it returns None.
        """
        for player in self.players:
            if player.chess_id == chess_id:
                return player
        return None

    def update_player(
        self, chess_id, first_name=None, last_name=None, birth_date=None
    ):
        """
        This function updates the information of a player based on
        the provided chess ID.if a matching player is found, it
        updates the player's attributes with the provided values.
        The updated list of players is then saved to the JSON file.
        If the provided chess ID does not match any player,
        an error message is displayed to the user.
        """
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
            print("Modifications des données joueur enregistrées")
        else:
            print("L'identifiant fournie ne correspond pas !!!")

    def delete_player(self, chess_id):
        """
        This function deletes a player based on the provided chess ID.
        If a matching player is found, the player is removed from the
        player list,the JSON file is updated and a success message
        is displayed. If the provided chess ID does not match any
        player, an error message is displayed.
        """
        player = self.get_player(chess_id)
        if player:
            self.players.remove(player)
            self.save_players()
            print("Suppression joueur effectuée avec succcès")
        else:
            print("L'identifiant fournie ne correspond pas !!!")

    def load_players(self):
        """
        This function loads the player data from the "players.json".
        It reads the JSON file and deserialize it into a list
        of player dictionaries. Each player dictionary is then
        converted back into a Player object using the from_dict()
        method,and the resulting player objects are stored in
        the self.players list.If the JSON file is not found or
        there is an error decoding it, the function sets self.players
        to an empty list.
        """
        try:
            with open("data/players.json", "r") as file:
                player_list = json.load(file)
                self.players = [
                    Player.from_dict(player) for player in player_list
                ]
        except (FileNotFoundError, json.JSONDecodeError):
            self.players = []

    def get_chess_id(self, prompt):
        """
        This function takes a prompt as input and ask the user to provide
        a chess ID.It then checks if the input complies with a regular
        expression pattern to ensure that the chess ID is in the correct
        format: two uppercase letters followed by five digits.
        It also checks if the provided chess ID exists in the player
        list using the player_exists() method. If the input is empty or
        does not match the pattern or the chess ID does not exist, error
        messages are displayed, and the user is asked to re-enter the
        chess ID until it matches the required format and corresponds
        to an existing player. The valid chess ID is then returned.
        """
        pattern = re.compile(r"^[A-Z]{2}\d{5}$")
        chess_id = input(prompt)
        while (
            not chess_id.strip()
            or not pattern.match(chess_id)
            or not self.player_exists(chess_id)
        ):
            if not chess_id.strip():
                print("Vous ne pouvez pas laisser le champ vide.")
            elif not pattern.match(chess_id):
                print(
                    "Format incorrect! L'ID d'échecs doit être composé "
                    "de 2 lettres majuscules suivies de 5 chiffres."
                )
            else:
                print("Aucun joueur avec cet ID d'échecs n'existe.")
            chess_id = input(prompt)
        return chess_id

    def player_exists(self, chess_id):
        """
        This function takes a chess_id as argument and checks if
        a player with the provided chess ID exists in the
        player list. It returns True if the player is
        found in the list; otherwise, it returns False.
        """
        return any(
            player.chess_id == chess_id for player in self.players
        )

    def update_player_score_by_chess_id(self, chess_id, new_score):
        """
        This function updates the score of a player based on
        chess ID.It searches for the player with the given
        chess ID in the player list.
        If a matching player is found, his score is increased
        by the new_score value. The updated list of players is
        then saved to the JSON file using the save_players() function.
        If the provided chess ID does not match any player,
        an error message is displayed.
        """
        for player in self.players:
            if player.chess_id == chess_id:
                player.score += new_score
                self.save_players()
                print(
                    f"Score du joueur avec l'identifiant {chess_id} "
                    f"mis à jour avec succès."
                )
                return
        print(f"Le joueur avec l'identifiant: {chess_id} n'existe pas.")

    def rank_players(self):
        """
        This function ranks the players based on their scores.
        It first sorts the players in descending order by score and
        creates a new list called sorted_players. Then, it updates
        each player's ranking based on their position in the
        sorted_players list. The player with the highest score
        will receive the rank of 1, the second-highest score will
        receive the rank of 2 ...
        The updated list of players, including their rankings,
        is saved to the JSON file using the
        """
        sorted_players = sorted(
            self.players, key=lambda player: player.score, reverse=True
        )
        for i, player in enumerate(sorted_players, start=1):
            player.ranking = i
        self.save_players()

    def valid_score(self, score):
        """
        This function takes a score as input and checks if it
        is a valid score for a match.
        A valid score can be 0 (lost), 0.5 (drawn), or 1 (won).
        If a valid score is provided,the function returns True,
        Otherwise, it returns False.
        """
        if score in [0, 0.5, 1]:
            return True
        else:
            return False

    def list_players_alphabetically(self):
        """
        This function lists all the players in the self.players list
        in alphabetical order based on their first names,creates
        a new list called sorted_players. Then, it iterates
        through the sorted_players list and prints the chess ID,
        first name, last name, and score of each player
        on separate lines.
        """
        sorted_players = sorted(
            self.players, key=lambda player: player.first_name
        )
        for player in sorted_players:
            print(
                f"Chess ID: {player.chess_id}, Prénom: {player.first_name},"
                f"Nom: {player.last_name}, Score: {player.score}"
            )
