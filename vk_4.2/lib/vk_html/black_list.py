from lib.vk_api.black_list import get_black_list


def black_list_html(name, token):
    template = r'''<div class="item" style="border-bottom: 1px solid #e7e8ec;">
<div class='item__main'><a href="{url}">{person_name}</a></div></div>'''

    black_list = get_black_list(token)

    f = open(r'users/%s/Список друзей и Чёрный список.txt' % name, 'a', encoding='utf-8')
    f.write('Чёрный список:\n')
    for i in range(len(black_list['items'])):
        url = black_list['items'][i]['url']
        name2 = '%s %s' % (black_list['items'][i]['first_name'], black_list['items'][i]['last_name'])
        f.write('   %s - %s\n' % (url, name2))
    f.close()

    content = ''
    for person in black_list['items']:
        person_name = '%s %s' % (person['first_name'], person['last_name'])
        url = person['url']
        content += template.format(person_name=person_name, url=url)

    s = r'''<!DOCTYPE html>
<html>
<head>
  <title>VK</title>
  <meta charset="UTF-8">
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
  <div class="page_block_header_inner _header_inner"><a class="ui_crumb" href="../index.html" onclick="return nav.go(this, event, {back: true});">Профиль</a><div class="ui_crumb_sep"></div><div class="ui_crumb" >Черный список</div></div>
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

    s %= content

    f = open(r'users/%s/%s/html/blacklist.html' % (name, name), 'w', encoding='utf-8')
    f.write(s)
    f.close()