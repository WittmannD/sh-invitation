from typing import Union

from src.connections import bot
from src.helpres import get_chat
from src.invitation import invitation_by_chat, invitation_by_user_list


def run_invitation_by_list(filepath: str, target_chat: Union[int, str]):
    chat_id = get_chat(target_chat)

    print(chat_id)

    if chat_id is None:
        raise ValueError('Неправильний формат посилання на чат')

    with open(filepath, 'r', encoding='utf-8') as file:
        bot.run(invitation_by_user_list((row for row in file), chat_id))


def run_invitation_by_chat(source_chat: Union[int, str], target_chat: Union[int, str], limit: int = -1):
    target_chat_id = get_chat(target_chat)
    source_chat_id = get_chat(source_chat)

    if target_chat_id is None or source_chat_id is None:
        raise ValueError('Неправильний формат посилання на чат')

    bot.run(invitation_by_chat(source_chat_id, target_chat_id, limit=limit))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(prog='Shadow invitation')
    subparsers = parser.add_subparsers(help='Тіньовий інвайтинг', dest='func')

    parser_a = subparsers.add_parser('by-list', help='Інвайтинг за списком користувачів')
    parser_a.add_argument('--file', '-f', action='store', required=True, type=str, help='Файл зі списком юзернеймів / id користувачів')
    parser_a.add_argument('--target-chat', '-t', action='store', required=True, type=str, help='ID або юзернейм цільового чату / каналу')

    parser_b = subparsers.add_parser('by-chat', help='Інвайтинг користувачів із чатів та каналів')
    parser_b.add_argument('--source-chat', '-s', action='store', required=True, type=str, help='ID або юзернейм чату з якого будуть взяті нові учасники')
    parser_b.add_argument('--limit', '-l', action='store', default=-1, type=int, help='Кількість учасників для інвайту')
    parser_b.add_argument('--target-chat', '-t', action='store', required=True, type=str, help='ID або юзернейм цільового чату / каналу')

    args = parser.parse_args()

    try:
        if args.func == 'by-list':
            run_invitation_by_list(args.file, args.target_chat)

        elif args.func == 'by-chat':
            run_invitation_by_chat(args.source_chat, args.target_chat, limit=args.limit)

    except ValueError as err:
        print(err)

