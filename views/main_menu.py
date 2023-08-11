class MainMenu:
    def __init__(self, player_controller, tournament_controller):
        self.player_controller = player_controller
        self.tournament_controller = tournament_controller

    def display_menu(
        self, menu_function, choices_dict, exit_choice=None
    ):
        while True:
            menu_function()
            choice = input("Choisissez une option: ")
            if exit_choice and choice == exit_choice:
                break
            choices_dict.get(choice, lambda: None)()

    def display(self):
        self.display_menu(
            self.player_controller.main_menu,
            {
                "1": self.player_menu_display,
                "2": self.tournament_menu_display,
                "3": self.report_menu_display,
                "4": exit,
            },
        )

    def player_menu_display(self):
        self.display_menu(
            self.player_controller.player_menu,
            {
                "1": self.player_controller.add_player_wrapper,
                "2": self.player_controller.update_player_wrapper,
                "3": self.player_controller.delete_player_wrapper,
                "4": self.player_controller.list_players_wrapper,
            },
            "5",
        )

    def tournament_menu_display(self):
        self.display_menu(
            self.tournament_controller.tournament_menu,
            {
                "1": self.tournament_controller.add_tournament_wrapper,
                "2": self.tournament_controller.tournament_list_wrapper,
                "3": self.tournament_controller.update_tournament_wrapper,
                "4": self.tournament_controller.delete_tournament_wrapper,
                "5": self.tournament_controller.start_round_wrapper,
                "6": self.tournament_controller.end_round_wrapper,
                "7": self.tournament_controller.add_match_to_round_wrapper,
                "8": self.tournament_controller.automatic_match_wrapper,
                "9": self.tournament_controller.update_match_wrapper,
            },
            "10",
        )

    def report_menu_display(self):
        self.display_menu(
            self.tournament_controller.report_menu,
            {
                "1": self.player_controller.list_players_alphabetically,
                "2": self.tournament_controller.short_tournament_list_wrapper,
                "3": self.tournament_controller.tournament_details_wrapper,
            },
            "4",
        )
