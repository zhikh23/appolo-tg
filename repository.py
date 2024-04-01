from aiogram import Bot
from base.singleton import Singleton
from config import Config


class Repository(metaclass=Singleton):
    config: Config
    tgbot: Bot
