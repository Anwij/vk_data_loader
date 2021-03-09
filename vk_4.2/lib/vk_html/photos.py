from lib.vk_api.photos import get_photos


def photos_html(name, token):
    header = r''' <h2 class="page_block_h2">
<div class="page_block_header clear_fix">
<div class="page_block_header_extra_left _header_extra_left"></div>
<div class="page_block_header_extra _header_extra"></div>
<div class="page_block_header_inner _header_inner"><div class="ui_crumb" >%s</div></div>
</div>'''

    template = r'''<div class="item">
<div class="item__main"><a href="{url}"><img src="{url}"></a></div>
<div class="item__tertiary">{date}</div>
</div>'''

    photos = get_photos(token)

    content = ''
    for t in ['saved', 'profile', 'wall']:
        if t == 'saved': text = 'Сохраненные фотографии'
        if t == 'profile': text = 'Фотографии профиля'
        if t == 'wall': text = 'Фотографии со стены'

        if photos[t]['count'] > 0:
            content += header % text

        for photo in photos[t]['items']:
            url = photo['url']
            date = photo['date']
            content += template.format(url=url, date=date)

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
  <div class="page_block_header_inner _header_inner"><a class="ui_crumb" href="../index.html" onclick="return nav.go(this, event, {back: true});">Профиль</a><div class="ui_crumb_sep"></div><div class="ui_crumb" >Фотографии</div></div>
</div>
</h2><div class="wrap_page_content">%s</div><!--/content-->

</div>
   </div>
   <div class="footer">

   </div>
  </div>
</body>
</html>'''

    s %= content

    f = open(r'users/%s/%s/html/photos.html' % (name, name), 'w', encoding='utf-8')
    f.write(s)
    f.close()