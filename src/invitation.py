import asyncio
from typing import Iterable, Union

from src.connections import bot
from src.helpres import chat_context, get_participants, get_user, validate_chat, validate_target_chat


async def invitation_by_user_list(users: Iterable[str], target_chat_id: Union[int, str]):
    async with bot:
        await validate_target_chat(target_chat_id)

        for user in users:
            try:
                await bot.add_chat_members(target_chat_id, user_ids=get_user(user))
                print(f'Користувач {user}, доданий до чату {target_chat_id}')
            except Exception as err:
                print(f'Не вдалось додати користувача {user}. Reason: {str(err)}')

            await asyncio.sleep(1)


async def invitation_by_chat(source_chat_id: Union[int, str], target_chat_id: Union[int, str], limit=-1):
    async with bot:
        await validate_chat(source_chat_id)
        await validate_target_chat(target_chat_id)

        async with chat_context(bot, source_chat_id) as source_chat:
            participants_generator = await get_participants(bot, source_chat)

            added = 0
            async for user in participants_generator:
                if added == limit:
                    break

                try:
                    await bot.add_chat_members(target_chat_id, user_ids=user.id)
                    print(f'Користувач {user.id}, доданий до чату {target_chat_id}')
                except Exception as err:
                    print(f'Не вдалось додати користувача {user.username or user.first_name}. Reason: {str(err)}')

                added += 1
                await asyncio.sleep(1)
