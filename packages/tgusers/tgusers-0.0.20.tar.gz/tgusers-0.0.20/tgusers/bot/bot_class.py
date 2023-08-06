import tgusers
import aiogram


from time import time
from tgusers.tables.users import User
from tgusers.tables.tables import Tables
from tgusers.tables.messages import Message
from aiogram import Bot, Dispatcher, executor, types
from tgusers.utils.runfunc import run_function_with_arguments_by_annotations
from tgusers.dataclasses.rooms import Arguments, Argument


class TelegramBot:
    def __init__(self, api_key: str, tables: Tables, rooms: list, message_logging: bool, antispam: bool = False):
        self.bot = Bot(api_key)
        self.disp = Dispatcher(self.bot)
        self.rooms = rooms
        self.tables = tables
        self.antispam = antispam
        self.spam_filter = {}
        self.max_messages_in_minute = 15
        self.last_list_update = time()
        self.message_logging = message_logging

        @self.disp.message_handler(content_types=['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact', 'sticker'])
        async def message_handler(message: types.Message):
            try:
                if self.antispam:
                    if time() - self.last_list_update > 60:
                        self.spam_filter = {}
                        self.last_list_update = time()
                    if not self.spam_filter.get(message.chat.id):
                        self.spam_filter[message.chat.id] = 1
                    else:
                        self.spam_filter[message.chat.id] += 1
                    if self.spam_filter.get(message.chat.id) > self.max_messages_in_minute:
                        await message.answer("Slower, slower. Not spam please.")
                        return
                user = self.reg_user(message=message)
                self.log(user, "text", message=message)
                o_args = [
                    Argument(value=message, annotation=types.Message)
                ]
                n_o_args = [
                    Argument(value=tgusers.Rooms(), annotation=tgusers.Rooms)
                ]
                for room in self.rooms:
                    if room.message_handler and message.content_type in room.content_type and (
                            room.name == user.room or room.is_global):
                        if room.not_obligatory_arguments:
                            n_o_args += room.not_obligatory_arguments
                        args = Arguments(obligatory=o_args, not_obligatory=n_o_args)
                        await run_function_with_arguments_by_annotations(room.function, args)
            except aiogram.utils.exceptions.BotBlocked:
                print(message.chat.id, "has blocked this bot")

        @self.disp.callback_query_handler()
        async def callback_query_handler(call: types.CallbackQuery):
            try:
                user = self.reg_user(call=call)
                self.log(user, "callback", call=call)
                o_args = [
                    Argument(value=call, annotation=types.CallbackQuery)
                ]
                n_o_args = [
                    Argument(value=tgusers.Rooms(), annotation=tgusers.Rooms)
                ]
                args = Arguments(obligatory=o_args, not_obligatory=n_o_args)
                for room in self.rooms:
                    if room.callback_query_handler and (room.name == user.room or room.is_global):
                        await run_function_with_arguments_by_annotations(room.function, args)
            except aiogram.utils.exceptions.BotBlocked:
                print(call.from_user.id, "has blocked this bot")


    def reg_user(self, message: types.Message = None, call: types.CallbackQuery = None):
        user = None
        if call:
            if not self.tables._users.check_user_for_registration(telegram_id=call.from_user.id):
                user = User(telegram_id=call.from_user.id, user_name=call.from_user.username,
                            language=call.from_user.language_code, role="user",
                            room="start")
                user.id = self.tables._users.add(user).get("id")
            else:
                user = self.tables._users.get_user(telegram_id=call.from_user.id)
        if message:
            if not self.tables._users.check_user_for_registration(message):
                user = User(telegram_id=message.chat.id, user_name=message.chat.username,
                            language=message.from_user.language_code, role="user",
                            room="start")
                user.id = self.tables._users.add(user).get("id")
            else:
                user = self.tables._users.get_user(message)
        return user

    def log(self, user: User, log_type: str, message: types.Message = None, call: types.CallbackQuery = None):
        if self.message_logging:
            if log_type == "text":
                log_message = Message(user_id=user.id, message=message.text, message_id=message.message_id,
                                      time=round(time()))
                self.tables._messages.add(log_message)
                print(message.chat.username, ":", message.chat.id, " -> ", message.text, "[", message.content_type, "]")
            if log_type == "callback":
                print("[ CALLBACK ]", call.from_user.username, ":", call.from_user.id, " -> ", call.data)

    def polling(self):
        executor.start_polling(self.disp, skip_updates=False)
