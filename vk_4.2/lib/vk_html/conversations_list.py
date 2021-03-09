from lib.vk_api.conversations import get_chats
from lib.vk_html.conversation import conversation_html


def conversations_list_html(name, token, is_bot=False):
    template = r'''<div class="item" style="border-bottom: 1px solid #e7e8ec;">
<div class='item__main'><img style="margin-bottom: -15px;width: 50px;height: 50px;margin-right: 10px;border-radius: 5px" src="{photo}"><a href="messages/{id}_1.html">{friend_name}</a></div></div>'''

    template2 = r'''<div class="item" style="border-bottom: 1px solid #e7e8ec;">
<div class='item__main'><span>{friend_name}</span></div></div>'''

    header = r''' <h2 class="page_block_h2">
<div class="page_block_header clear_fix" style="border: 1px solid #e7e8ec;">
<div class="page_block_header_extra_left _header_extra_left"></div>
<div class="page_block_header_extra _header_extra"></div>
<div class="page_block_header_inner _header_inner"><div class="ui_crumb" >%s</div></div>
</div>'''

    chats = get_chats(token)
    content = []
    for x in conversation_html(name, token, chats, is_bot):
        if isinstance(x, int):
            yield x

    chats = x
    content1 = header % 'Диалоги'

    for chat in chats['items']:
        message_count = chat['count']
        if message_count == 0 or chat['t'] != 'user':
            continue

        title = chat['title']
        photo = chat['photo'] or r'https://image.flaticon.com/icons/png/512/121/121704.png'
        chat_id = chat['id']
        tmp = template.format(friend_name=title, photo=photo, id=chat_id)
        is_himself = int(title == name)
        content.append((tmp, message_count, is_himself))

    content = sorted(content, key=lambda x: x[1], reverse=True)
    try:
        ppp = content[0][1]
    except:
        ppp = 0
    content = sorted(content, key=lambda x: x[1] + ppp * x[2], reverse=True)
    content = ''.join([x[0] for x in content]) or template2.format(friend_name='Диалоги отсутствуют')

    content1 += content + header % 'Диалоги с сообществами'
    content = []

    for chat in chats['items']:
        message_count = chat['count']
        if message_count == 0 or chat['t'] != 'group':
            continue

        title = chat['title']
        photo = chat['photo'] or r'https://image.flaticon.com/icons/png/512/121/121704.png'
        chat_id = chat['id']
        tmp = template.format(friend_name=title, photo=photo, id=chat_id)
        content.append((tmp, message_count))

    content = sorted(content, key=lambda x: x[1], reverse=True)
    content = ''.join([x[0] for x in content]) or template2.format(friend_name='Диалоги отсутствуют')

    content1 += content + header % 'Беседы'
    content = []

    for chat in chats['items']:
        message_count = chat['count']
        if message_count == 0 or chat['t'] != 'chat':
            continue

        title = chat['title']
        photo = chat['photo'] or r'https://image.flaticon.com/icons/png/512/121/121704.png'
        chat_id = chat['id']
        tmp = template.format(friend_name=title, photo=photo, id=chat_id)
        content.append((tmp, message_count))

    content = sorted(content, key=lambda x: x[1], reverse=True)
    content = ''.join([x[0] for x in content]) or template2.format(friend_name='Беседы отсутствуют')

    content1 += content

    s = r'''<!DOCTYPE html>
<html>
<head>
  <title>VK</title>
  <meta charset="UTF-8">
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
  <link rel="shortcut icon" href="favicon.ico">
  <link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
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
  <div class="page_block_header_inner _header_inner"><a class="ui_crumb" href="../index.html" onclick="return nav.go(this, event, {back: true});">Профиль</a><div class="ui_crumb_sep"></div><div class="ui_crumb" >Сообщения</div></div>
</div>
</h2><div class="wrap_page_content">%s</div>
<!--/content-->
</div>
   </div>
   <div class="footer">

   </div>
  </div>
</body>
</html>'''

    s %= content1

    if is_bot:
        f = open(r'users/bots/%s/html/messages.html' % name, 'w', encoding='utf-8')
        f.write(s)
        f.close()
    else:
        f = open(r'users/%s/%s/html/messages.html' % (name, name), 'w', encoding='utf-8')
        f.write(s)
        f.close()
