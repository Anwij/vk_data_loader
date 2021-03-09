def investments_html(name, cid, photos, videos):
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
            a > img {
                width: 200px;
                height: 200px;
            }
        </style>
      <div class="wrap">
        <div class="header">
      <div class="page_header">
        <div class="top_home_logo"></div>
      </div>
    </div>
        <div class="page_content clear_fix" style="width: 100%%;">
    <div class="page_block">
    <!--content-->
     <h2 class="page_block_h2">
    <div class="page_block_header clear_fix">
      <div class="page_block_header_extra_left _header_extra_left"></div>
      <div class="page_block_header_extra _header_extra"></div>
      <div class="page_block_header_inner _header_inner"><a class="ui_crumb" href="%d_1.html" onclick="return nav.go(this, event, {back: true});">Сообщения</a><div class="ui_crumb_sep"></div><div class="ui_crumb" >Вложения</div>
      <div class="ui_crumb" style="float: right;">
    <a href="v%d.html">Видеозаписи</a>
</div>
</div>
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

    s2 = r'''<!DOCTYPE html>
        <html>
        <head>
          <title>VK</title>
          <meta charset="UTF-8">
          <link rel="shortcut icon" href="../favicon.ico">
          <link rel="stylesheet" type="text/css" href="../style.css">
        </head>
        <body>
          <div class="wrap">
            <div class="header">
          <div class="page_header">
            <div class="top_home_logo"></div>
          </div>
        </div>
            <div class="page_content clear_fix" style="width: 100%%;">
        <div class="page_block">
        <!--content-->
         <h2 class="page_block_h2">
        <div class="page_block_header clear_fix">
          <div class="page_block_header_extra_left _header_extra_left"></div>
          <div class="page_block_header_extra _header_extra"></div>
          <div class="page_block_header_inner _header_inner"><a class="ui_crumb" href="%d_1.html" onclick="return nav.go(this, event, {back: true});">Сообщения</a><div class="ui_crumb_sep"></div><div class="ui_crumb" >Вложения</div>
          <div class="ui_crumb" style="float: right;">
        <a href="i%d.html">Фотографии</a>
    </div>
    </div>
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

    table = r'''<table style="width: 100%;">
  <tbody>'''
    table2 = r'''</tbody></table>'''

    content = table

    for i in range(0, len(photos), 6):
        tmp = photos[i: i + 6]
        content += r'<tr>'
        for x in tmp:
            content += r'<th>'
            content += r'<a href="{url}" ><img src="{photo}"></a><div><a href="{cid}_{ind}.html#n{mess_id}">Перейти к сообщению</a></div>'.format(url=x['body']['url'], photo=x['body']['photo'], cid=cid, ind=x.get('ind', 1), mess_id=x['id'])
            content += r'</th>'
        content += r'</tr>'
    content += table2
    s = s % (cid, cid, content)


    f = open(r'users/%s/%s/html/messages/i%d.html' % (name, name, cid), 'w', encoding='utf-8')
    f.write(s)
    f.close()

    ###################################################

    table = r'''<table style="width:100%;">
     <tbody>'''
    table2 = r'''</tbody></table>'''

    content = table

    for i in range(0, len(videos), 6):
        tmp = videos[i: i + 6]
        content += r'<tr>'
        for x in tmp:
            content += r'<th>'
            content += r'<a href="{url}"><img style="width: 200px; height: 200px;" src="{photo}"></a>'.format(
                url=x['body']['url'], photo=x['body']['photo'])
            content += r'</th>'
        content += r'</tr>'
    content += table2
    s2 = s2 % (cid, cid, content)

    f = open(r'users/%s/%s/html/messages/v%d.html' % (name, name, cid), 'w', encoding='utf-8')
    f.write(s2)
    f.close()

