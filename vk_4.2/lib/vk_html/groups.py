from lib.vk_api.groups import get_groups


def groups_html(name, token):
    template = r'''<div class="item" style="border-bottom: 1px solid #e7e8ec;">
<div class='item__main'><img style="margin-bottom: -15px;width: 50px;height: 50px;margin-right: 10px;border-radius: 5px" src="{photo}"><a href="{url}">{group_name}</a></div></div>'''

    groups = get_groups(token)

    content = ''
    for group in groups['items']:
        group_name = group['name']
        url = group['url']
        photo = group['photo']
        content += template.format(group_name=group_name, url=url, photo=photo)

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
  <div class="page_block_header_inner _header_inner"><a class="ui_crumb" href="../index.html" onclick="return nav.go(this, event, {back: true});">Профиль</a><div class="ui_crumb_sep"></div><div class="ui_crumb" >Сообщества</div></div>
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

    f = open(r'users/%s/%s/html/groups.html' % (name, name), 'w', encoding='utf-8')
    f.write(s)
    f.close()