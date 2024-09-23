from tgbot.config import Config


class DataBase:

    def __init__(self, config: Config):
        self.config = config

    def create_tables(self):
        print("Tables created (they are not)")