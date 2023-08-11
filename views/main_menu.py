class MainMenu:
    def __init__(self, player_controller, tournament_controller):
        self.player_controller = player_controller
        self.tournament_controller = tournament_controller

    def display(self):
        while True:
            self.player_controller.main_menu()
            choice = input("Choisissez une option: ")
            main_menu_choices = {
                "1": self.player_menu_display,
                "2": self.tournament_menu_display,
                "3": self.report_menu_display,
                "4": exit,
            }
            main_menu_choices.get(
                choice, lambda: print("Option invalide")
            )()

    def player_menu_display(self):
        while True:
            self.player_controller.player_menu()
            choice = input("Choisissez une option: ")
            player_menu_choices = {
                "1": self.player_controller.add_player_wrapper,
                "2": self.player_controller.update_player_wrapper,
                "3": self.player_controller.delete_player_wrapper,
                "4": self.player_controller.list_players_wrapper,
                "5": lambda: None,
            }
            player_menu_choices.get(
                choice, lambda: print("Option invalide")
            )()
            if choice == "5":
                break

    def tournament_menu_display(self):
        while True:
            self.tournament_controller.tournament_menu()
            choice = input("Choisissez une option: ")

            if choice == "10":
                break

            tournament_menu_choices = {
                "1": self.tournament_controller.add_tournament_wrapper,
                "2": self.tournament_controller.tournament_list_wrapper,
                "3": self.tournament_controller.update_tournament_wrapper,
                "4": self.tournament_controller.delete_tournament_wrapper,
                "5": self.tournament_controller.start_round_wrapper,
                "6": self.tournament_controller.end_round_wrapper,
                "7": self.tournament_controller.add_match_to_round_wrapper,
                "8": self.tournament_controller.automatic_match_wrapper,
                "9": self.tournament_controller.update_match_wrapper,
            }
            tournament_menu_choices.get(
                choice, lambda: print("Option invalide")
            )()

    def report_menu_display(self):
        while True:
            self.tournament_controller.report_menu()
            choice = input("Choisissez une option: ")
            if choice == "4":
                break
            main_menu_choices = {
                "1": self.player_controller.list_players_alphabetically,
                "2": self.tournament_controller.short_tournament_list_wrapper,
                "3": self.tournament_controller.tournament_details_wrapper,
            }
            main_menu_choices.get(
                choice, lambda: print("Option invalide")
            )()
