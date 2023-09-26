import re
from contextlib import asynccontextmanager, contextmanager
from typing import Union

from pyrogram import Client
from pyrogram.errors import UsernameInvalid, exceptions
from pyrogram.types import Chat, ChatPreview
from pyrogram.enums import ChatType

from src.connections import bot

USERNAME_RE = re.compile(
    r'@|(?:https?://)?(?:www\.)?(?:telegram\.(?:me|dog)|t\.me)/(@|\+|joinchat/)?'
)
TG_JOIN_RE = re.compile(
    r'tg://(join)\?invite='
)

VALID_USERNAME_RE = re.compile(
    r'^[a-z](?:(?!__)\w){1,30}[a-z\d]$',
    re.IGNORECASE
)


def get_user(entity: Union[str, int]):
    if type(entity) == int or (type(entity) == str and entity.isnumeric()):
        return int(entity)

    if entity[:4] == "http":
        return entity[13:]

    return entity


def get_chat(entity: Union[str, int]):
    if type(entity) == int or (type(entity) == str and entity.isnumeric()):
        return int(entity)

    username_or_hash, _ = parse_username(entity)
    return username_or_hash


async def validate_chat(chat_id: Union[str, int]):
    try:
        chat = await bot.get_chat(chat_id)

    except ValueError:
        raise ValueError(f'Не вдалось знайти чат {chat_id}')

    if chat.type == ChatType.PRIVATE or chat.type == ChatType.BOT:
        raise ValueError('Неправильний тип чату')


async def validate_target_chat(chat_id: Union[str, int]):
    try:
        chat = await bot.get_chat(chat_id)

    except (ValueError, UsernameInvalid):
        raise ValueError(f'Не вдалось знайти чат {chat_id}, або він має обмежений доступ')

    if type(chat) == ChatPreview:
        raise ValueError('Бот повинен бути членом цільового чату / каналу та мати привілеї для інвайту')

    if chat.type == ChatType.PRIVATE or chat.type == ChatType.BOT:
        raise ValueError('Неправильний тип чату')


async def get_channel_participants(client: Client, channel: Chat):
    supergroup = await get_linked_chat(client, channel)
    viewed = set()

    try:
        async for message in client.get_chat_history(supergroup.id, limit=10_000):
            user = message.from_user

            if user is None or user.id in viewed:
                continue

            viewed.add(user.id)
            yield message.from_user

    except Exception as err:
        print('get_channel_participants', err)


async def get_linked_chat(client: Client, chat: Chat):
    if hasattr(chat, 'linked_chat') and chat.linked_chat is not None:
        return chat.linked_chat


async def get_participants(client: Client, chat: Chat):
    if chat.type == ChatType.CHANNEL:
        return get_channel_participants(client, chat)

    return client.get_chat_members(chat.id)


def parse_username(username: str):
    """
    Parses the given username or channel access hash, given
    a string, username or URL. Returns a tuple consisting of
    both the stripped, lowercase username and whether it is
    a joinchat/ hash (in which case is not lowercase'd).

    Returns ``(None, False)`` if the ``username`` or link is not valid.
    """
    username = username.strip()
    m = USERNAME_RE.match(username) or TG_JOIN_RE.match(username)
    if m:
        username = username[m.end():]
        is_invite = bool(m.group(1))
        if is_invite:
            return username, True
        else:
            username = username.rstrip('/')

    if VALID_USERNAME_RE.match(username):
        return username.lower(), False
    else:
        return None, False


@asynccontextmanager
async def chat_context(client: Client, chat_entity: Union[int, str]):
    chat = None
    username_or_hash, _ = parse_username(chat_entity)

    try:
        try:
            await client.join_chat(username_or_hash)
        except exceptions.UserAlreadyParticipant:
            pass

        chat = await client.get_chat(username_or_hash)

        yield chat

    except exceptions.InviteRequestSent:
        raise ValueError('Канал приватний')

    finally:
        if chat and hasattr(chat, 'id'):
            await client.leave_chat(chat.id)
