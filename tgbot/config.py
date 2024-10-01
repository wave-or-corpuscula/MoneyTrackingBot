from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    database : str


@dataclass
class TgBot:
    token : str
    admin_ids : list
    use_redis : bool
    use_webhooks : bool


@dataclass
class BotSettings:
    max_spending_types_amount : int
    max_spending_type_len : int


@dataclass
class Config:
    tg_bot : TgBot
    db : DbConfig
    bot_settings: BotSettings


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
            use_webhooks=env.bool("USE_WEBHOOKS"),
        ),
        db=DbConfig(
            database=env.str('DB_NAME')
        ),
        bot_settings=BotSettings(
            max_spending_types_amount=env.int("MAX_SPENDING_TYPES_AMOUNT"),
            max_spending_type_len=env.int("MAX_SPENDING_TYPE_LEN")
        )
    )
