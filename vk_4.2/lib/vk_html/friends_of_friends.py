from lib.vk_api.tools import send_request


def friends_of_friends_html(name, token, friends):
    s = r'''<!DOCTYPE html>
    <html>
    <head>
      <title>VK</title>
      <meta charset="UTF-8">
      <link rel="shortcut icon" href="favicon.ico">
      <link rel="stylesheet" type="text/css" href="style.css">
    </head>
    <body>
    <style>
        i {
            border-bottom: 1px solid #e7e8ec; margin-left: 50px;
        }
        .item__main > img {
            margin-bottom: -15px;width: 50px;height: 50px;margin-right: 10px;border-radius: 5px
        }
        .i1 {
            padding: 20px 0;
            word-wrap: break-word;
        }
        .i2 {
            padding: 20px 0;
            margin-left: 50px;
            word-wrap: break-word;
            border-bottom: 1px solid #e7e8ec;
        }
        
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
      <div class="page_block_header_inner _header_inner"><a class="ui_crumb" href="../index.html" onclick="return nav.go(this, event, {back: true});">Профиль</a><div class="ui_crumb_sep"></div><div class="ui_crumb" >Друзья друзей</div></div>
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

    template = r'''<div class="i1">
        <div class='item__main'><img src="{photo}"><a href="{url}">{friend_name}</a></div></div>'''

    template2 = r'''<div class="i2">
        <div class='item__main'><img src="{photo}"><a href="{url}">{friend_name}</a></div></div>'''

    content = ''

    header = r''' <h2 class="page_block_h2">
    <div class="page_block_header clear_fix" style="border: 1px solid #e7e8ec; height: 90px;">
    <div class="page_block_header_extra_left _header_extra_left"></div>
    <div class="page_block_header_extra _header_extra"></div>
    <div class="page_block_header_inner _header_inner"><div class="ui_crumb" >%s</div></div>
    </div>'''

    f = open(r'users/%s/Список друзей друзей.txt' % name, 'w', encoding='utf-8')
    f.write('Список друзей друзей пользователя (%s):\n\n' % name)

    fc = len(friends[:250])
    fi = 0
    p = 0
    yield 0

    for ind, user_friend in enumerate(friends[:250]):
        name2 = '%s %s' % (user_friend['first_name'], user_friend['last_name'])
        f.write('   Друзья пользователя (%s):\n' % name2)

        fi += 1
        if int(fi / fc * 100) > p:
            p = int(fi / fc * 100)
            yield int(fi / fc * 100)
        content += header % template.format(url=user_friend['url'], photo=user_friend['photo'], friend_name='%s %s' % (user_friend['first_name'], user_friend['last_name']))
        response = send_request(None, 'friends.get', token=token, extra_data='&user_id=%s&count=250&order=hints&fields=photo_50' % user_friend['id'])
        if not response.get('response', ''):
            continue
        for friend in response['response']['items']:
            url = 'https://vk.com/id%d' % friend['id']
            photo = friend.get('photo_50', '')
            content += template2.format(url=url, photo=photo, friend_name='%s %s' % (friend['first_name'], friend['last_name']))
            f.write('       %s - %s\n' % (url, '%s %s' % (friend['first_name'], friend['last_name'])))
        f.write('\n')

    f.close()

    s %= content

    f = open(r'users/%s/%s/html/friends_of_friends.html' % (name, name), 'w', encoding='utf-8')
    f.write(s)
    f.close()

