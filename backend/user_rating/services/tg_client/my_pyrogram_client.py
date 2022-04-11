import asyncio
from pyrogram.errors import SessionPasswordNeeded, BadRequest
from pyrogram.types import User
from pyrogram.utils import ainput
from pyrogram import Client


from .confirmation_code_bot.bot import request_confirmation_code


class MyPyrogramClient(Client):
    async def authorize(self) -> User:
        if self.bot_token:
            return await self.sign_in_bot(self.bot_token)

        while True:
            try:
                if not self.phone_number:
                    raise Exception('You must pass a phone number as a required argument')

                sent_code = await self.send_code(self.phone_number)
            except BadRequest as e:
                print(e.MESSAGE)
                self.phone_number = None
                self.bot_token = None
            else:
                break

        if self.force_sms:
            sent_code = await self.resend_code(self.phone_number, sent_code.phone_code_hash)

        print("The confirmation code has been sent via {}".format(
            {
                "app": "Telegram app",
                "sms": "SMS",
                "call": "phone call",
                "flash_call": "phone flash call"
            }[sent_code.type]
        ))

        while True:
            if not self.phone_code:
                # self.phone_code = await ainput("Enter confirmation code: ")
                self.phone_code = request_confirmation_code()

            try:
                signed_in = await self.sign_in(self.phone_number, sent_code.phone_code_hash, self.phone_code)
            except BadRequest as e:
                print(e.MESSAGE)
                self.phone_code = None
            except SessionPasswordNeeded as e:
                print(e.MESSAGE)

                while True:
                    print("Password hint: {}".format(await self.get_password_hint()))

                    if not self.password:
                        self.password = await ainput("Enter password (empty to recover): ", hide=self.hide_password)

                    try:
                        if not self.password:
                            confirm = await ainput("Confirm password recovery (y/n): ")

                            if confirm == "y":
                                email_pattern = await self.send_recovery_code()
                                print(f"The recovery code has been sent to {email_pattern}")

                                while True:
                                    recovery_code = await ainput("Enter recovery code: ")

                                    try:
                                        return await self.recover_password(recovery_code)
                                    except BadRequest as e:
                                        print(e.MESSAGE)
                                    except Exception as e:
                                        # log.error(e, exc_info=True)
                                        raise
                            else:
                                self.password = None
                        else:
                            return await self.check_password(self.password)
                    except BadRequest as e:
                        print(e.MESSAGE)
                        self.password = None
            else:
                break

        if isinstance(signed_in, User):
            return signed_in
