from controllers.players_controller import PlayerController
from controllers.tournament_controller import TournamentController
from views.main_menu import MainMenu


def main():
    player_controller = PlayerController()
    tournament_controller = TournamentController()
    main_menu = MainMenu(player_controller, tournament_controller)
    main_menu.display()


if __name__ == "__main__":
    main()
