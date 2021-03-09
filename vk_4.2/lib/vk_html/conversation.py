from lib.vk_api.conversations import get_conversations
from time import time
from math import ceil
from lib.vk_html.investment import investments_html
from lib.vk_api.docs import get_docs
from lib.vk_api.black_list import get_black_list


def conversation_html(name, token, chats, is_bot):
    s = r'''<!DOCTYPE html>
    <html>
    <head>
      <title>VK</title>
      <meta charset="UTF-8">
      <link rel="shortcut icon" href="../favicon.ico">
      <link rel="stylesheet" type="text/css" href="../style.css">
    </head>
    <body>
    <style>
    .item {
        padding: 10px 0 0 0;
    }
    
    .message__header > img {
        width: 50px; height: 50px; border-radius: 5px; margin-right: 10px; margin-bottom: -10px;
    }
    .k {
        margin-top: 15px;
    }
    .i {
        padding: 10px 0;
        word-wrap: break-word;
        border-bottom: 1px solid #e7e8ec;
    }
    
    .t {
    width: 50px;
    height: 50px;
    display: inline-block;
    border-radius: 5px;
    margin-right: 10px;
    margin-bottom: -10px;
    }
    
    .i > a {
    display: inline-block;
    margin-bottom: 15px;
    }
    
    .l {
        margin-left: 50px;
        margin-top: 10px; 
    }
    
    %s
    </style>
      <div class="wrap">
        <div class="header">
      <div class="page_header">
        <div class="top_home_logo"></div>
      </div>
    </div>
        <div class="page_content clear_fix">
    <div class="page_block">
    <!--content-->
     <h2 class="page_block_h2">
    <div class="page_block_header clear_fix">
      <div class="page_block_header_extra_left _header_extra_left"></div>
      <div class="page_block_header_extra _header_extra"></div>
      <div class="page_block_header_inner _header_inner"><a class="ui_crumb" href="../messages.html" onclick="return nav.go(this, event, {back: true});">Сообщения</a><div class="ui_crumb_sep"></div><div class="ui_crumb" >%s</div><div class="ui_crumb" style="float: right;">
    <a href="#n%d">Перейти в конец</a>
</div>
<div class="ui_crumb" style="float: right;margin-right: 75px;">
    <a href="i%d.html">Вложения</a>
</div></div>
    </div>
    </h2><div class="wrap_page_content">%s</div>
    <!--/content-->
    </div>
       </div>
       <div class="footer">
                   <div style="
    text-align: center;
    font-size: 18px;
"><span>Страницы</span></div>
            %s
       </div>
       </div>
      </div>
    </body>
    </html>'''


    st = r'''.t%d {background-image: url("%s");}
'''

    template = r'''<div class="i" id="n{num}"><div class="t{d} t"></div><a href="{user_url}">{user_name}</a>, {date}<div>{body}{att}</div></div>'''

    at = r'''<div class="attachment">
    <div>{attachment}</div>
    <div class="attachment__description">{t}</div>
    </div>'''

    template0 = r'''<div class="i" id="n{num}">
    <div class="message__header"><img src="{url}"><a href="{user_url}">{user_name}</a>, {date}</div>
    <div class="k">{body}{att}</div></div>'''

    nav = r'''<nav style="
    text-align: center;
    font-size: 20px;
    /* display: block; */
    line-height: 1.5em;">'''
    nav2 = '''</nav>'''

    for x in get_conversations(token, chats):
        if isinstance(x, int):
            yield x

    messages = x
    #f = open(r'data/%s/messages.txt' % name, 'w', encoding='utf-8')
    l = len(messages['items'])

    li = '''<a href="{id}_{num}.html" id="p{num}" style="margin: 0 5px 0 5px;">{num}</a>'''

    li2 = '''<a href="{id}_{num}.html" id="p{num}">{num}</a>'''

    last_id = 0
    y = 0 + min(1, len(get_docs(token)['items'])) + min(1, len(get_black_list(token)['items']))
    for chat_ind in range(len(messages['items'])):
        style = ''
        d = {}
        r = 0
        for person in messages['items'][chat_ind]['users']:
            if not d.get(person['photo'], None):
                d[person['photo']] = r
                style += st % (r, person['photo'])
                r += 1
        photos = []
        videoss = []
        if messages['items'][chat_ind]['count'] == 0:
            continue

        chat_id = messages['items'][chat_ind]['id']
        chat_name = messages['items'][chat_ind]['title']

        footer = nav
        for ind in range(ceil(len(messages['items'][chat_ind]['items']) / 2000)):
            footer += li.format(id=chat_id, num=ind + 1)
        footer += nav2

        ind = 1
        for j in range(len(messages['items'][chat_ind]['items']) - 1, -1, -2000):
            if is_bot:
                f = open(r'users/bots/%s/html/messages/%d_%d.html' % (name, chat_id, ind), 'w', encoding='utf-8')
            else:
                f = open(r'users/%s/%s/html/messages/%d_%d.html' % (name, name, chat_id, ind), 'w', encoding='utf-8')
            ind += 1
            content = '<style>#p%d {text-decoration: underline}</style>' % (ind - 1)
            for i in range(j, max(j - 2000, -1), -1):
                last_id = messages['items'][chat_ind]['items'][i]['id']
                messages['items'][chat_ind]['items'][i]['ind'] = ind - 1
                dd = d[messages['items'][chat_ind]['items'][i]['from_user']['photo']]
                content += get_mess_html(messages['items'][chat_ind]['items'][i], template, at, photos, videoss, dd, d)

            f.write(s % (style, chat_name, last_id, chat_id, content, footer))
            f.close()

        if not is_bot:
            investments_html(name, chat_id, photos, videoss)

    yield messages


def get_mess_html(message, template, at, photos, videoss, d1, d):
    user_name = '%s %s' % (message['from_user']['first_name'], message['from_user']['last_name'])
    user_url = message['from_user']['url']
    date = message['date']
    photo = message['from_user']['photo']

    if message['t'] == 'text':
        t = ''
        body = message['body']['text']
        attachment = ''
    elif message['t'] == 'photo':
        photos.append(message)
        t = 'Фотография'
        body = message['body']['text']
        attachment = '<a href="%s"><img style="padding-top: 10px;" src="%s"></a>' % (message['body']['url'], message['body']['url'])
    elif message['t'] == 'video':
        videoss.append(message)
        t = 'Видео'
        body = message['body']['text']
        attachment = '<a href="%s"><img src="%s" style="padding-top: 10px; display: block"><span style="display: block;margin: 10px 0 10px 0">%s</span></a>' % (
            message['body']['url'], message['body']['photo'], message['body']['title'])
    elif message['t'] == 'audio':
        t = 'Аудиозапись'
        body = message['body']['text']
        attachment = '<span class="archive__page-icon archive__page-icon--audio-albums" style="padding-left: 10px;padding-right: 10px;padding-bottom: 2px;line-height: 35px"></span><a href="%s">%s</a>' % (
        message['body']['url'], message['body']['title'])
    elif message['t'] == 'sticker':
        t = 'Стикер'
        body = ''
        attachment = '<img src="%s">' % message['body']['photo']
    elif message['t'] == 'call':
        t = 'Звонок'
        body = ''
        attachment = '<b><i>*Звонок*</i></b>'
    elif message['t'] == 'doc':
        t = 'Документ'
        body = message['body']['text']
        attachment = '<a href=%s>%s</a>' % (message['body']['url'], message['body']['title'])
    elif message['t'] == 'gift':
        t = 'Подарок'
        body = message['body']['message']
        attachment = '<img src="%s">' % message['body']['photo']
    elif message['t'] == 'wall':
        t = 'Запись на стене'
        body = message['body']['text']
        attachment = '<a href=%s>%s</a>' % (message['body']['url'], message['body']['url'])
    elif message['t'] == 'link':
        t = 'Ссылка'
        body = message['body']['text']
        attachment = '<a href=%s>%s</a>' % (message['body']['url'], message['body']['url'])
    elif message['t'] == 'market':
        t = 'Товар'
        body = message['body']['text']
        attachment = '<img src="%s"><a style="display: block" href="%s">%s</a><div>%s</div>' % (message['body']['photo'], message['body']['url'], message['body']['url'], message['body']['title'])
    elif message['t'] == 'fwd':
        t = 'Пересланное сообщение'
        body = message['body']['text']
        attachment = ''
        for y in message['body']['messages']:
            x = y[0]
            d2 = d[y[1]['photo']]
            fwd_mess = get_mess_html(x, template, at, photos, videoss, d2, d)
            fwd_mess = fwd_mess[:5] + r'''class="l i" ''' + fwd_mess[5:]
            attachment += fwd_mess
    elif message['t'] == 'wall_reply':
        t = 'Комментарий к записи'
        body = message['body']['text']
        attachment = '<b><i>*Комментарий к записи*</i></b>'
    elif message['t'] == 'market_album':
        t = 'Подборка товаров'
        body = message['body']['text']
        attachment = '<b><i>*Подборка товаров*</i></b>'
    elif message['t'] == 'action':
        t = 'Действие'
        body = ''
        attachment = '<b><i>%s</i></b>' % message['body']['action']
    elif message['t'] == 'podcast':
        t = 'Подкаст'
        body = ''
        attachment = '<b><i>%s</i></b>' % message['body']['title']

    if (not attachment) and (not t):
        att = ''
    else:
        att = at.format(attachment=attachment, t=t)

    return template.format(user_name=user_name, user_url=user_url, date=date, d=d1, body=body, att=att, num=message['id'])