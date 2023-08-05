import re
import traceback
from dataclasses import dataclass
from typing import *

import pyrogram.types
from pyrogram.types import Update

from botkit.future_tgtypes.chat import Chat
from botkit.future_tgtypes.message import Message
from botkit.future_tgtypes.message_descriptor import MessageDescriptor
from botkit.tghelpers.entities.message_entities import ParsedEntity, parse_entities


@dataclass
class UpdateFieldExtractor:  # TODO: implement properly
    update: Update

    @property
    def chat(self) -> Optional[Chat]:
        if isinstance(self.update, pyrogram.types.Message):
            return self.update.chat
        return None

    @property
    def user(self) -> Optional[Chat]:
        if isinstance(self.update, pyrogram.types.Message):
            return self.update.from_user
        return None

    @property
    def chat_id(self) -> Optional[int]:
        return chat.id if (chat := self.chat) else None

    @property
    def user_id(self) -> int:
        return user.id if (user := self.user) else None

    @property
    def message_descriptor(self) -> Optional[MessageDescriptor]:
        return MessageDescriptor.from_update(self.update)

    @property
    def message_id(self) -> Optional[Union[int, str]]:
        return descriptor.message_id if (descriptor := self.message_descriptor) else None

    @property
    def message_text(self) -> Optional[str]:
        if hasattr(self.update, "text"):
            return self.update.text

    @property
    def command_name(self) -> Optional[str]:
        if hasattr(self.update, "command"):  # Pyrogram
            return self.update.command[0]

    @property
    def command_args(self) -> Optional[List[str]]:
        if hasattr(self.update, "command"):  # Pyrogram
            return self.update.command[1:]

    @property
    def command_args_str(self) -> Optional[str]:
        return " ".join(self.command_args) if self.command_args else None

    @property
    def replied_to_message(self) -> Optional[Message]:
        # TODO: turn into protocols
        if isinstance(self.update, pyrogram.types.Message):
            return self.update.reply_to_message

    @property
    def replied_to_message_id(self) -> Optional[int]:
        return reply_msg.message_id if (reply_msg := self.replied_to_message) else None

    @property
    def matches(self) -> Optional[List[re.Match]]:
        if hasattr(self.update, "matches"):
            return self.update.matches

    @property
    def entities(self) -> List[ParsedEntity]:
        try:
            # noinspection PydanticTypeChecker
            return parse_entities(self.update)
        except Exception as ex:
            traceback.print_exc(ex)
            return []
