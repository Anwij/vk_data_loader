from lib.vk_api.gifts import get_gifts


def gifts_html(name, token):
    template = r'''<div class="item">
<div class="item__main"><img src="{photo}" alt="1087"></div><div class="item__main">{message}</div>
<div class="item__tertiary"><a href="{from_url}" class="mem_link">{from_url}</a> {date}</div>
</div>'''

    gifts = get_gifts(token)

    content = ''
    for gift in gifts['items']:
        from_url = gift['from_url']
        photo = gift['photo']
        message = gift['message']
        date = gift['date']
        content += template.format(from_url=from_url, photo=photo, message=message, date=date)

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
  <div class="page_block_header_inner _header_inner"><a class="ui_crumb" href="../index.html" onclick="return nav.go(this, event, {back: true});">Профиль</a><div class="ui_crumb_sep"></div><div class="ui_crumb" >Подарки</div></div>
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

    f = open(r'users/%s/%s/html/gifts.html' % (name, name), 'w', encoding='utf-8')
    f.write(s)
    f.close()