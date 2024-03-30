from dataclasses import dataclass
from environs import Env


@dataclass
class SaverConfig:
    addr: str


@dataclass
class RegisterConfig:
    addr: str


@dataclass
class BotConfig:
    token: str


@dataclass
class Config:
    bot: BotConfig
    saver: SaverConfig
    register: RegisterConfig


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        bot=BotConfig(
            token=env("TG_BOT_TOKEN"),
        ),
        saver=SaverConfig(
            addr=env("SAVER_ADDR"),
        ),
        register=RegisterConfig(
            addr=env("REGISTER_ADDR")
        )
    )
