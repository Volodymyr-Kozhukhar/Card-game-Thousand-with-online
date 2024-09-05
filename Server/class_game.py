

class Game:

    __players = {}      # (connection number (player number), connection)
    __game_name = ""

    def __init__(self, name):
        self.__game_name = name

    def new_player(self):
        pass