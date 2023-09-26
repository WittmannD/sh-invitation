```shell
python main.py --help

#    usage: Shadow invitation [-h] {by-list,by-chat} ...
#    
#    positional arguments:
#      {by-list,by-chat}  Тіньовий інвайтинг
#        by-list          Інвайтинг за списком користувачів
#        by-chat          Інвайтинг користувачів із чатів та каналів
#    
#    options:
#      -h, --help         show this help message and exit

python main.py by-list --help

#    usage: Shadow invitation by-list [-h] --file FILE --target-chat TARGET_CHAT
#    
#    options:
#      -h, --help            show this help message and exit
#      --file FILE, -f FILE  Файл зі списком юзернеймів / id користувачів
#      --target-chat TARGET_CHAT, -t TARGET_CHAT
#                            ID або юзернейм цільового чату / каналу

python main.py by-chat --help

#    usage: Shadow invitation by-chat [-h] --source-chat SOURCE_CHAT [--limit LIMIT] --target-chat TARGET_CHAT
#    
#    options:
#      -h, --help            show this help message and exit
#      --source-chat SOURCE_CHAT, -s SOURCE_CHAT
#                            ID або юзернейм чату з якого будуть взяті нові учасники
#      --limit LIMIT, -l LIMIT
#                            Кількість учасників для інвайту
#      --target-chat TARGET_CHAT, -t TARGET_CHAT
#                            ID або юзернейм цільового чату / каналу

```