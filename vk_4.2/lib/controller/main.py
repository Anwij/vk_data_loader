import shutil
import traceback
from time import time
from typing import *
import os

from lib.tools.get_accounts import get_user_token
from lib.vk_html.black_list import black_list_html
from lib.vk_html.conversations_list import conversations_list_html
from lib.vk_html.docs import docs_html
from lib.vk_html.friends import friends_html
from lib.vk_html.gifts import gifts_html
from lib.vk_html.groups import groups_html
from lib.vk_html.index import index_html
from lib.vk_html.info import page_info_html
from lib.vk_html.photos import photos_html
from lib.vk_html.stories import stories_html
from lib.vk_html.videos import videos_html

from lib.controller.response import Response
from lib.controller.account import Account


class Main:
    def __init__(self):
        self.account = None
        if not os.path.exists(r'tokens'):
            os.mkdir(r'tokens')
        if not os.path.exists(r'users'):
            os.mkdir(r'users')

    def load_accounts(self) -> None:
        token = get_user_token()
        self.account = Account(token)

    def load_data(self, account: Account) -> Iterator[Response]:
        try:
            t = time()
            token = account.token
            name = account.name

            yield Response('Загрузка пользователя (%s)' % name)

            if os.path.exists(r'users/%s' % name):
                shutil.rmtree(r'users/%s' % name)

            os.mkdir(r'users/%s' % name)
            os.mkdir(r'users/%s/%s' % (name, name))
            os.mkdir(r'users/%s/%s/html' % (name, name))
            os.mkdir(r'users/%s/%s/html/messages' % (name, name))
            shutil.copy('files_to_copy/favicon.ico', 'users/%s/%s/html/favicon.ico' % (name, name))
            shutil.copy('files_to_copy/style.css', 'users/%s/%s/html/style.css' % (name, name))

            index_html(name, token)
            page_info_html(name, token)
            yield Response('    Загрузка фотографий')
            photos_html(name, token)
            yield Response('    Загрузка видеозаписей')
            videos_html(name, token)
            yield Response('    Загрузка друзей и друзей друзей')
            for x in friends_html(name, token):
                yield Response(x, response_type=Response.Type.PERCENT)
            yield Response('    Загрузка групп')
            groups_html(name, token)
            yield Response('    Загрузка чёрного списка')
            black_list_html(name, token)
            yield Response('    Загрузка документов')
            docs_html(name, token)
            yield Response('    Загрузка подарков')
            gifts_html(name, token)
            yield Response('    Загрузка историй')
            stories_html(name, token)
            yield Response('    Загрузка сообщений')
            for x in conversations_list_html(name, token):
                yield Response(x, response_type=Response.Type.PERCENT)

            yield Response('    Загрузка завершена', response_type=Response.Type.SEPARATOR)

            delta = time() - t
            yield Response('Выполнено за %.2f сек\n' % delta)
        except:
            yield Response(traceback.format_exc(), response_type=Response.Type.ERROR)



