import os
import telebot
from dotenv import dotenv_values
from .file_tools import read_from_file, write_to_file

BASEDIR = os.path.abspath(os.path.dirname(__file__))
config = dotenv_values(os.path.join(BASEDIR, '.env'))
TG_TOKEN = config['TG_TOKEN']
ADMIN_USER_ID = int(config['ADMIN_USER_ID'])
current_dir = os.path.dirname(os.path.realpath(__file__))
LAST_MSG_ID_FILENAME = f"{current_dir}/last_msg_id.txt"


class ConfirmationCodeBot:
    INVALID_CODE_MSG = "Код не прошёл валидацию, отправьте еще раз"

    def __init__(self):
        self.bot = telebot.TeleBot(TG_TOKEN, threaded=False)
        self._code = None

        @self.bot.message_handler(content_types=['text'])
        def get_text_messages(message):
            if message.message_id <= self._last_msg_id:
                return
            else:
                self._last_msg_id = message.message_id

            if message.from_user.id == ADMIN_USER_ID:
                print(f'NEW MESSAGE FROM ADMIN {message}')
                msg_text = self._prepare_message(message.text)
                code: int | bool = self._validate_confirmation_code(msg_text)
                if code is False:
                    self.send_message(ADMIN_USER_ID, self.INVALID_CODE_MSG)
                else:
                    self.code = code
            else:
                print(f'Message from unallowed user: {message}')

    @property
    def _last_msg_id(self) -> int:
        data = read_from_file(LAST_MSG_ID_FILENAME)
        if not data:
            return -1
        try:
            last_msg_id = int(data)
        except ValueError as e:
            return -1
        return last_msg_id

    @_last_msg_id.setter
    def _last_msg_id(self, msg_id: int):
        write_to_file(str(msg_id), LAST_MSG_ID_FILENAME)

    @property
    def code(self) -> int | None:
        return self._code

    @code.setter
    def code(self, val: int):
        self._code = val
        self.bot.stop_polling()

    def send_message(self, user_id: int, msg: str):
        self.bot.send_message(user_id, msg)

    def _prepare_message(self, msg: str):
        msg = msg.strip()
        msg = msg.replace('\n', ' ')
        msg = msg.replace('  ', ' ')
        return msg

    def _validate_confirmation_code(self, code: str) -> int | bool:
        try:
            code = int(code)
        except Exception as e:
            print(f'Validation error! {e}')
            return False

        if len(str(code)) != 5:
            return False

        return code

    def request_confirmation_code(self, info: str) -> int:
        msg = 'Запрошен код подтвердения для авторизации в клиенте'
        if info:
            msg += f'\n {info}'
        self.send_message(ADMIN_USER_ID, msg)
        self.bot.polling(none_stop=True, interval=0)
        return self.code


def request_confirmation_code(info: str = "") -> str:
    tg_bot = ConfirmationCodeBot()
    code = str(tg_bot.request_confirmation_code(info))
    tg_bot.bot.stop_polling()
    return code



