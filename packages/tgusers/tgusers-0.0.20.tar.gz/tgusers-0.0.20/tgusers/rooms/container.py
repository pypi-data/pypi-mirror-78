from random import randint


from tgusers.dataclasses.rooms import Room
from tgusers.utils.validator import valid_check
from tgusers.errors.rooms import RoomsErrors
from tgusers.utils.arguments_container import ArgumentsContainer, ArgumentsBox

class RoomsContainer: ...


class RoomsContainer:
    def __init__(self):
        self.rooms = []

    def add_message_room(self, name: str = None, content_type: list = None, roles: list = None,
                         is_global: bool = False):
        if roles is None:
            roles = ["all"]
        if content_type is None:
            content_type = []
        if name is None:
            name = str(randint(100000, 999999))
        if not valid_check(name):
            raise RoomsErrors("Invalid room name")

        def decorator(room_func):
            if is_global:
                room = Room(name=name, content_type=content_type, roles=roles, function=room_func, is_global=True,
                            message_handler=True)
                self.rooms.append(room)
            else:
                room = Room(name=name, content_type=content_type, roles=roles, function=room_func, is_global=False,
                            message_handler=True)
                self.rooms.append(room)

        return decorator

    def add_callback_room(self, name: str = None, is_global: bool = False):
        if name is None:
            name = str(randint(100000, 999999))
        if not valid_check(name):
            raise RoomsErrors("Invalid room name")

        def decorator(room_func):
            room = Room(name=name, roles=[], function=room_func, is_global=is_global, callback_query_handler=True)
            self.rooms.append(room)

        return decorator

    def on_join_room(self, name: str = None):
        def decorator(fuc):
            self.get_room_by_name(name).on_join = fuc

        return decorator


    def get_room_by_name(self, name) -> Room:
        for room in self.rooms:
            if room.name == name:
                return room
        return None

    def upload_rooms(self, rooms_container: RoomsContainer):
        self.rooms += rooms_container.rooms


    def upload_external_arguments(self, arguments: ArgumentsContainer):
        for room_arguments in arguments.arguments_list:
            room_arguments: ArgumentsBox
            room_name = room_arguments.room_name
            arguments = room_arguments.arguments
            for get_room_name in self.rooms:
                if get_room_name.name == room_name:
                    if not get_room_name.not_obligatory_arguments:
                        get_room_name.not_obligatory_arguments = []
                    get_room_name.not_obligatory_arguments += arguments

