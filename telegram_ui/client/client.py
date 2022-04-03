import os
from typing import List
from pyrogram import Client
from tools.singleton import Singleton
from dotenv import dotenv_values


class ClientError(Exception): pass
class ClientConfigError(ClientError): pass


BASEDIR = os.path.abspath(os.path.dirname(__file__))
config = dotenv_values(os.path.join(BASEDIR, 'client.env'))
if 'CHAT_ID' not in config or 'API_ID' not in config or 'API_HASH' not in config:
    raise ClientConfigError('Invalid config file')

try:
    CHAT_ID = int(config['CHAT_ID'])
    API_ID = int(config['API_ID'])
    API_HASH = config['API_HASH']
except ValueError as e:
    raise ClientConfigError(f'Invalid config value: {e}')


class Reaction:
    def __init__(self, emoji: str, num: int):
        self.emoji = emoji
        self.num = num

    def __str__(self):
        return f'{self.emoji}: {self.num}'

    def __repr__(self):
        return f'Reaction {self.__str__()}'


class Message:
    def __init__(self, id_: int, text: str, reactions: List[Reaction]):
        self.id_ = id_
        self.text = text
        self.reactions = reactions

    def __str__(self):
        return f'{self.id_}: "{self.text}" {self.reactions}'

    def __repr__(self):
        return f'Message {self.__str__()}'


class MyClient(metaclass=Singleton):
    def __init__(self, chat_id: int = CHAT_ID):
        self.app = Client("user_bot_client", api_id=API_ID, api_hash=API_HASH)
        self.chat_id = chat_id

    def get_messages_with_reactions(self) -> List[Message]:
        with self.app:
            messages = []
            history = self.app.get_history(chat_id=self.chat_id, limit=100)
            for message in history:
                if message.reactions:
                    reactions = [Reaction(reaction.emoji, reaction.count) for reaction in message.reactions]
                    message_obj = Message(message.message_id, message.text, reactions)
                    messages.append(message_obj)
        return messages

