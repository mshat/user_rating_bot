import os
from typing import List
from .my_pyrogram_client import MyPyrogramClient
from dotenv import dotenv_values
from .confirmation_code_bot.file_tools import read_from_file, write_to_file


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
    PHONE_NUMBER = config['PHONE_NUMBER']
except ValueError as e:
    raise ClientConfigError(f'Invalid config value: {e}')


current_dir = os.path.dirname(os.path.realpath(__file__))
AUTHORIZE_CODE_SENT_FILENAME = f"{current_dir}/authorization_code_sent.txt"


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


class MyClient:
    def __init__(self, chat_id: int = CHAT_ID):
        self.chat_id = chat_id

        self.app = MyPyrogramClient("user_bot_client", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUMBER)
        if not self.is_user_authorized:
            print('Юзер не авторизован в клиенте, запускаю авторизацию')
            self._authorize()

    @property
    def is_user_authorized(self) -> bool:
        try:
            self.app.get_me()
        except ConnectionError:
            return False

        self.authorization_process_already_started = False
        return True

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

    @property
    def authorization_process_already_started(self) -> bool:
        authorization_process_already_started = read_from_file(AUTHORIZE_CODE_SENT_FILENAME)
        if authorization_process_already_started == '1':
            return True
        else:
            return False

    @authorization_process_already_started.setter
    def authorization_process_already_started(self, flag: bool):
        if flag:
            print('ЗАПИСЫВАЮ В ФАЙЛ 1')
            write_to_file('1', AUTHORIZE_CODE_SENT_FILENAME)  # Ставим флаг о том, что авторизация запущена
        else:
            print('ЗАПИСЫВАЮ В ФАЙЛ 0')
            write_to_file('0', AUTHORIZE_CODE_SENT_FILENAME)  # Ставим флаг о том, что авторизация завершена

    def _authorize(self):
        print('МЕТОД АВТОРИЗАЦИИ')
        if self.authorization_process_already_started:
            print('АВТОРИЗАЦИЯ УЖЕ БЫЛА ЗАПУЩЕНА, НЕ ВЫЁБЫВАЮСЬ')
            return  # Авторизация уже была запущена, ничего делать не нужно
        else:
            print('АВТОРИЗАЦИЯ ЕЩЕ НЕ БЫЛА ЗАПУЩЕНА, ЗАПУСКАЮ')
            self.authorization_process_already_started = True

            with self.app:
                self.app.get_history(chat_id=self.chat_id, limit=1)


if __name__ == '__main__':
    client = MyClient()
    print(client.get_messages_with_reactions())

