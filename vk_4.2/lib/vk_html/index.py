from lib.vk_api.info import get_info


def index_html(name, token, is_bot=False):
    info = get_info(token)
    url = info['url']

    s = r'''<!DOCTYPE html>
<html>
<head>
  <title>VK</title>
  <meta charset="UTF-8">
  <link rel="shortcut icon" href="html/favicon.ico">
  <link rel="stylesheet" type="text/css" href="html/style.css">
</head>
<body>
  <div class="wrap">
    <div class="header">
  <div class="page_header">
    <div class="top_home_logo"></div>
  </div>
</div>
    <div class="page_content clear_fix">
<div class="menu">
<!--menu-->
<div class="page_block">
<h2 class="page_block_h2">
<div class="page_block_header clear_fix">
  <div class="page_block_header_extra_left _header_extra_left"></div>
  <div class="page_block_header_extra _header_extra"></div>
  <div class="page_block_header_inner _header_inner">{name} (<a href="{url}">{url}</a>)</div>
</div>
</h2>
<div class="wrap_page_content">
  <div class="item">
  <div class='item__main'><div class="index-row">
  <a class="menu__page-link" href="html/page-info.html">
    <span class="archive__page-icon archive__page-icon--page-info"></span>
    <div>Информация о странице</div>
  </a>
</div></div>


</div><div class="item">
  <div class='item__main'><div class="index-row">
  <a class="menu__page-link" href="html/friends.html">
    <span class="archive__page-icon archive__page-icon--friends"></span>
    <div> Друзья</div>
  </a>
</div></div>


</div><div class="item">
  <div class='item__main'><div class="index-row">
  <a class="menu__page-link" href="html/friends_of_friends.html">
    <span class="archive__page-icon archive__page-icon--external-contacts"></span>
    <div> Друзья друзей</div>
  </a>
</div></div>


</div><div class="item">
  <div class='item__main'><div class="index-row">
  <a class="menu__page-link" href="html/gifts.html">
    <span class="archive__page-icon archive__page-icon--gifts"></span>
    <div>Подарки</div>
  </a>
</div></div>


</div><div class="item">
  <div class='item__main'><div class="index-row">
  <a class="menu__page-link" href="html/groups.html">
    <span class="archive__page-icon archive__page-icon--subscriptions"></span>
    <div>Группы</div>
  </a>
</div></div>


</div><div class="item">
  <div class='item__main'><div class="index-row">
  <a class="menu__page-link" href="html/blacklist.html">
    <span class="archive__page-icon archive__page-icon--blacklist"></span>
    <div>Чёрный список</div>
  </a>
</div></div>


</div><div class="item">
  <div class='item__main'><div class="index-row">
  <a class="menu__page-link" href="html/messages.html">
    <span class="archive__page-icon archive__page-icon--index-messages"></span>
    <div>Сообщения</div>
  </a>
</div></div>


</div><div class="item">
  <div class='item__main'><div class="index-row">
  <a class="menu__page-link" href="html/photos.html">
    <span class="archive__page-icon archive__page-icon--photo-albums"></span>
    <div>Фотографии</div>
  </a>
</div></div>


</div><div class="item">
  <div class='item__main'><div class="index-row">
  <a class="menu__page-link" href="html/videos.html">
    <span class="archive__page-icon archive__page-icon--video-albums"></span>
    <div>Видео</div>
  </a>
</div></div>


</div><div class="item">
  <div class='item__main'><div class="index-row">
  <a class="menu__page-link" href="html/stories.html">
    <span class="archive__page-icon archive__page-icon--stories"></span>
    <div>Истории</div>
  </a>
</div></div>


</div><div class="item">
  <div class='item__main'><div class="index-row">
  <a class="menu__page-link" href="html/docs.html">
    <span class="archive__page-icon archive__page-icon--documents"></span>
    <div>Документы</div>
  </a>
</div></div>


</div>
</div>
</div>


<!--/menu-->
</div>
</body>
</html>'''.format(name=name, url=url)

    s1 = r'''<!DOCTYPE html>
    <html>
    <head>
      <title>VK</title>
      <meta charset="UTF-8">
      <link rel="shortcut icon" href="html/favicon.ico">
      <link rel="stylesheet" type="text/css" href="html/style.css">
    </head>
    <body>
      <div class="wrap">
        <div class="header">
      <div class="page_header">
        <div class="top_home_logo"></div>
      </div>
    </div>
        <div class="page_content clear_fix">
    <div class="menu">
    <!--menu-->
    <div class="page_block">
    <h2 class="page_block_h2">
    <div class="page_block_header clear_fix">
      <div class="page_block_header_extra_left _header_extra_left"></div>
      <div class="page_block_header_extra _header_extra"></div>
      <div class="page_block_header_inner _header_inner">{name} (<a href="{url}">{url}</a>)</div>
    </div>
    </h2>
    <div class="wrap_page_content">
      <div class="item">
      <div class='item__main'><div class="index-row">
      <a class="menu__page-link" href="html/page-info.html">
        <span class="archive__page-icon archive__page-icon--page-info"></span>
        <div>Информация о странице</div>
      </a>
    </div></div>


    </div><div class="item">
      <div class='item__main'><div class="index-row">
      <a class="menu__page-link" href="html/messages.html">
        <span class="archive__page-icon archive__page-icon--index-messages"></span>
        <div>Сообщения</div>
      </a>
    </div></div>


    </div>
    </div>
    </div>


    <!--/menu-->
    </div>
    </body>
    </html>'''.format(name=name, url=url)

    if is_bot:
        f = open(r'users/bots/%s/index.html' % name, 'w', encoding='utf-8')
        f.write(s1)
        f.close()
    else:
        f = open(r'users/%s/%s/index.html' % (name, name), 'w', encoding='utf-8')
        f.write(s)
        f.close()

