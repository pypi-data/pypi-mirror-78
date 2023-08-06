from typing import Any
from dataclasses import dataclass


@dataclass
class Room:
    name: str
    roles: list
    function: any
    on_join: any = None
    is_global: bool = False
    content_type: list = None
    message_handler: bool = False
    callback_query_handler: bool = False
    not_obligatory_arguments: list = None


@dataclass
class Argument:
    value: str
    annotation: Any


@dataclass
class Arguments:
    obligatory: list
    not_obligatory: list


