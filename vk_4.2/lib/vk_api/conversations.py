from math import ceil

from lib.vk_api.tools import send_request, transform_date
from lib.vk_api.info import get_info


def get_conversations(token, chats):
    data = chats

    http = None

    info = get_info(token)
    first_name = info['first_name']
    last_name = info['last_name']
    user_id = info['id']
    user_url = info['url']
    user_photo = info['photo']

    user = {
        'first_name': first_name,
        'last_name': last_name,
        'url': user_url,
        'id': user_id,
        'photo': user_photo
    }

    fc = len(chats['items'])
    fi = 0
    p = 0
    yield 0

    little_chats = []

    for i in range(len(chats['items'])):
        little_chats.append((chats['items'][i], i))

    yield 1


    line = r'''var chats%d = API.messages.getHistory({"extended": 1, "fields":"photo_50", "count": 200, "peer_id": %d, "access_token": "%s"});'''

    big_chats = []

    m = 0

    for k in range(0, len(little_chats), 10):
        tmp = r'''var data = ['''
        code = ''
        for index, chat in enumerate(little_chats[k:k + 10]):
            code += line % (index, chat[0]['id'], token)
            tmp += 'chats%d,' % index

        tmp = tmp[:-1:]
        tmp = code + tmp + ']; return data;'

        extra_data = '&code=%s' % tmp
        response = send_request(http, 'execute', token, extra_data)

        for ind, x in enumerate(response['response']):
            data['items'][little_chats[k + ind][1]]['count'] = x['count']
            data['items'][little_chats[k + ind][1]]['type'] = little_chats[k + ind][0]['t']
            if x['count'] > 200:
                big_chats.append(little_chats[k + ind])
            else:
                m += 1

                fi += 1
                if int(fi / fc * 100) > p:
                    p = int(fi / fc * 100)
                    yield int(fi / fc * 100)

                profiles = []
                profiles.extend(x.get('profiles', []))
                profiles.extend(x.get('groups', []))
                persons = get_chat_members(profiles)['items']
                for message in x['items']:
                    message_id = get_cmess(message, user, user_id, persons, little_chats[k + ind][1], data, token, [])[0]
                data['items'][little_chats[k + ind][1]]['users'] = persons

    for chat in big_chats:

        fi += 1
        if int(fi / fc * 100) > p:
            p = int(fi / fc * 100)
            yield int(fi / fc * 100)

        extra_data = '&extended=1&fields=photo_50&count=200&peer_id=%d' % chat[0]['id']
        response = send_request(http, 'messages.getHistory', token, extra_data)
        messages_count = response['response']['count']

        data['items'][chat[1]]['count'] = messages_count

        raw_messages = response['response']['items'][:-1:]
        message_id = response['response']['items'][-1]['id']

        code = r'''var data = [];
        var sm = %d;
        var i = 25;
        var chats = [];
        while (i > 0) {
            data.push(API.messages.getHistory({"extended": 1, "fields":"photo_50", "count": 200, "start_message_id": sm, "peer_id": %d, "access_token": "%s"}));
            if (data[data.length - 1].items.length == 200)
                sm = data[data.length - 1].items[data[data.length - 1].items.length - 1].id;
            else
                i = 0;
            i = i - 1;
        }
        return data;'''

        profiles = []
        g = ceil(messages_count / (25 * 199))
        if chat[0]['t'] != 'user':
            g = 1
        else:
            g = min(g, 8)

        for j in range(g):
            extra_data = '&code=%s' % (code % (message_id, chat[0]['id'], token))
            response = send_request(http, 'execute', token, extra_data)
            for x in response.get('response', []):
                profiles.extend(x.get('profiles', []))
                profiles.extend(x.get('groups', []))
                message_id = x['items'][-1]['id']
                raw_messages.extend(x['items'][:-1:])

        videos = []
        persons = get_chat_members(profiles)['items']

        for message in raw_messages:
            message_id = get_cmess(message, user, user_id, persons, chat[1], data, token, videos, is_big=1)[0]

        data['items'][chat[1]]['users'] = persons[::-1]

        for k in range(0, len(videos), 100):
            extra_data = '&videos=%s' % ( (','. join([x[0] for x in videos[k:k + 100]]))[:-1:] )
            response = send_request(http, 'video.get', token, extra_data)
            for ind, x in enumerate(response['response']['items']):
                if x.get('files', {}).get('mp4_1080', ''):
                    url = x.get('files', {})['mp4_1080']
                elif x.get('files', {}).get('mp4_720', ''):
                    url = x.get('files', {})['mp4_720']
                elif x.get('files', {}).get('mp4_480', ''):
                    url = x.get('files', {})['mp4_480']
                elif x.get('files', {}).get('mp4_360', ''):
                    url = x.get('files', {})['mp4_360']
                elif x.get('files', {}).get('mp4_240', ''):
                    url = x.get('files', {})['mp4_240']
                else:
                    url = ''

                data['items'][chat[1]]['items'][videos[ind][1]]['body']['url'] = url

    yield data


def get_chats(token):
    http = None

    line = r'''var chats%d = API.messages.getConversations({"extended": 1, "fields":"photo_50", "count": 200, "offset": %d, "access_token": "%s"});'''

    extra_data = '&extended=1&fields=photo_50&count=200&'
    response = send_request(http, 'messages.getConversations', token, extra_data)
    chats_count = min(response['response']['count'], 5000)
    raw_chats = response['response']['items']
    extra_data = '&extended=1&fields=photo_50&count=200'
    info = get_info(token)
    raw_chats.append({
        'conversation': {
            'peer': {
                'id': info['id'],
                'type': 'user'
            }
        }
    })

    tmp = '''var data = ['''
    code = ''
    if chats_count > 8000000:
        for i in range(1, ceil(chats_count / 200)):
            offset = i * 200
            code += line % (i, offset, token)
            tmp += 'chats%d,'% i

        tmp = tmp[:-1:]

        tmp = code + tmp + ']; return data;'
        if code:
            extra_data = '&code=%s' % tmp
            response = send_request(http, 'execute', token, extra_data)

            for x in response['response']:
                raw_chats.extend(x['items'])

    else:
        for i in range(1, ceil(chats_count / 200)):
            extra_data = '&extended=1&fields=photo_50&count=200&offset=%d' % (i * 200)
            response = send_request(http, 'messages.getConversations', token, extra_data)
            raw_chats.extend(response['response']['items'])

    data = {
        'count': chats_count,
        'items': []
    }

    c = {
        'group': [],
        'chat': [],
        'user': []
    }

    for chat in raw_chats:
        if chat['conversation']['peer']['type'] == 'chat':
            c['chat'].append(chat)
        elif chat['conversation']['peer']['type'] == 'group':
            c['group'].append(chat)
        elif chat['conversation']['peer']['type'] == 'user':
            c['user'].append(chat)

    if c['chat']:
        for x in c['chat']:
            p = x.get('conversation', {}).get('chat_settings', {}).get('photo', {})
            p = (
                p.get('photo_50', '') or
                p.get('photo_100', '') or
                p.get('photo_200', '')
            )
            title = x.get('conversation', {}).get('chat_settings', {}).get('title', {})
            data['items'].append({
                'id': x['conversation']['peer']['id'],
                'title': title,
                'photo': p,
                't': 'chat',
                'items': [],
                'count': 0
            })

    if c['group']:
        for i in range(300, len(c['group']), 300):
            extra_data = '&group_ids=%s' % ','.join([str(x['conversation']['peer']['local_id']) for x in c['group'][i - 300:i]])
            response = send_request(http, 'groups.getById', token, extra_data)

            for x in response['response']:
                title = x['name']
                p = x.get('photo_50', '') or x.get('photo_100', '')
                c_id = x['id']

                data['items'].append({
                    'id': c_id,
                    'title': title,
                    'photo': p,
                    't': 'group',
                    'items': [],
                    'count': 0
                })

        l = len(c['group'])
        extra_data = '&group_ids=%s' % ','.join([str(x['conversation']['peer']['local_id']) for x in c['group'][l - (l % 300):l]])
        response = send_request(http, 'groups.getById', token, extra_data)

        for x in response['response']:
            title = x['name']
            p = x.get('photo_50', '') or x.get('photo_100', '')
            c_id = x['id']

            data['items'].append({
                'id': c_id,
                'title': title,
                'photo': p,
                't': 'group',
                'items': [],
                'count': 0
            })

    if c['user']:
        for i in range(300, len(c['user']), 300):
            extra_data = '&fields=photo_50&user_ids=%s' % ','.join([str(x['conversation']['peer']['id']) for x in c['user'][i - 300:i]])
            response = send_request(http, 'users.get', token, extra_data)

            for x in response['response']:
                title = '%s %s' % (x['first_name'], x['last_name'])
                p = x['photo_50']
                c_id = x['id']

                data['items'].append({
                    'id': c_id,
                    'title': title,
                    'photo': p,
                    't': 'user',
                    'items': [],
                    'count': 0
                })

        l = len(c['user'])
        extra_data = '&fields=photo_50&user_ids=%s' % ','.join([str(x['conversation']['peer']['id']) for x in c['user'][l - (l % 300):l]])
        response = send_request(http, 'users.get', token, extra_data)

        for x in response['response']:
            title = '%s %s' % (x['first_name'], x['last_name'])
            p = x['photo_50']
            c_id = x['id']

            data['items'].append({
                'id': c_id,
                'title': title,
                'photo': p,
                't': 'user',
                'items': [],
                'count': 0
            })

    return data


def get_chat_members(response):
    members_count = len(response)
    members = response

    data = {
        'count': members_count,
        'items': []
    }

    for member in members:
        if not (member.get('first_name', '') or member.get('last_name', '')):
            first_name = member.get('name', '')
            last_name = ''
            url = 'https://vk.com/id%s' % member['screen_name']
            id = member['id']
        else:
            first_name = member.get('first_name', '')
            last_name = member.get('last_name', '')
            url = 'https://vk.com/id%s' % member['id']
            id = member['id']
        data['items'].append({
            'id': id,
            'first_name': first_name,
            'last_name': last_name,
            'photo': member['photo_50'],
            'url': url
        })
        #print(len(data['items']))

    return data


def get_cmess(message, user, user_id, persons, i, data, token, videos, message_id=None, is_big=0):
    http = None
    body = message['body']
    date = transform_date(message['date'])
    if not message_id: message_id = message['id']
    from_id = message.get('from_id', '') or message['user_id']

    if 1 == 2:
        from_user = user
    else:
        for member in persons:
            if from_id == member['id']:
                from_user = member
                break
            elif from_id == -member['id']:
                from_user = member
                break
        else:
            extra_data = '&fields=photo_50&user_ids=%d' % from_id
            response = send_request(http, 'users.get', token, extra_data)
            if response.get('response', ''):
                first_name = response['response'][0]['first_name']
                last_name = response['response'][0]['last_name']
                p = response['response'][0]['photo_50']
            else:
                extra_data = '&group_id=%d' % -from_id
                response = send_request(http, 'groups.getById', token, extra_data)
                if response.get('response', 0) != 0:
                    first_name = response['response'][0]['name']
                    last_name = ''
                    p = response['response'][0].get('photo_50', '') or response['response'][0].get('photo_100', '')
                else:
                    first_name = 'UNDEFINED'
                    last_name = ''
                    p = ''

            from_user = {
                'url': 'https://vk.com/id%s' % from_id,
                'first_name': first_name,
                'last_name': last_name,
                'id': from_id,
                'photo': p
            }

            persons.append(from_user)

    if message.get('attachments', ''):
        l = len(message['attachments'])
        tmp = body
        for (ind, x) in enumerate(message['attachments']):
            if ind + 1 != l:
                body = ''
            else:
                body = tmp

            if x['type'] == 'photo':
                if x['photo'].get('photo_1280', ''):
                    p = x['photo']['photo_1280']
                elif x['photo'].get('photo_807', ''):
                    p = x['photo']['photo_807']
                if x['photo'].get('photo_604', ''):
                    p = x['photo']['photo_604']
                elif x['photo'].get('photo_130', ''):
                    p = x['photo']['photo_130']
                elif x['photo'].get('photo_75', ''):
                    p = x['photo']['photo_75']

                if x['photo'].get('photo_604', ''):
                    pp = x['photo']['photo_604']
                if x['photo'].get('photo_130', ''):
                    pp = x['photo']['photo_130']
                elif x['photo'].get('photo_75', ''):
                    pp = x['photo']['photo_75']

                data['items'][i]['items'].append({
                    'id': message_id,
                    'from_user': from_user,
                    't': 'photo',
                    'date': date,
                    'body': {
                        'text':	body,
                        'url': p,
                        'photo': pp
                    }
                })

            elif x['type'] == 'sticker':
                data['items'][i]['items'].append({
                    'id': message_id,
                    'from_user': from_user,
                    't': 'sticker',
                    'date': date,
                    'body': {
                        'photo': (
                            x['sticker'].get('photo_64', '') or
                            x['sticker'].get('photo_128', '') or
                            x['sticker'].get('photo_256', '')
                        )
                    }
                })

            elif x['type'] == 'audio':
                data['items'][i]['items'].append({
                    'id': message_id,
                    'from_user': from_user,
                    't': 'audio',
                    'date': date,
                    'body': {
                        'url': x['audio']['url'],
                        'title': x['audio']['title'],
                        'text': body,
                    }
                })

            elif x['type'] == 'video':
                if x['video'].get('player', None):
                    url = x['video']['player']
                elif x['video'].get('is_private', 0) == 1 and not (x['video'].get('can_play', None) == 0 or x['video'].get('duration', None) == 0):
                    if is_big:
                        videos.append(('%s_%s_%s' % (x['video']['owner_id'], x['video']['id'], x['video']['access_key']), len(data['items'][i]['items'])))
                        url = ''
                    else:
                        extra_data = '&videos=%s_%s_%s' % (x['video']['owner_id'], x['video']['id'], x['video']['access_key'])
                        response = send_request(http, 'video.get', token, extra_data)
                        if response['response']['items'][0].get('files', {}).get('mp4_1080', ''):
                            url = response['response']['items'][0].get('files', {})['mp4_1080']
                        elif response['response']['items'][0].get('files', {}).get('mp4_720', ''):
                            url = response['response']['items'][0].get('files', {})['mp4_720']
                        elif response['response']['items'][0].get('files', {}).get('mp4_480', ''):
                            url = response['response']['items'][0].get('files', {})['mp4_480']
                        elif response['response']['items'][0].get('files', {}).get('mp4_360', ''):
                            url = response['response']['items'][0].get('files', {})['mp4_360']
                        elif response['response']['items'][0].get('files', {}).get('mp4_240', ''):
                            url = response['response']['items'][0].get('files', {})['mp4_240']
                        else:
                            url = ''

                else:
                    url = 'https://vk.com/video%s_%s' % (x['video']['owner_id'], x['video']['id'])

                if x['video'].get('photo_807', ''):
                    p = x['video']['photo_807']
                elif x['video'].get('photo_320', ''):
                    p = x['video']['photo_320']
                elif x['video'].get('photo_130', ''):
                    p = x['video']['photo_130']

                data['items'][i]['items'].append({
                    'id': message_id,
                    'from_user': from_user,
                    't': 'video',
                    'date': date,
                    'body': {
                        'title': x['video']['title'],
                        'photo': p,
                        'url': url,
                        'text': body
                    }
                })

            elif x['type'] == 'gift':
                data['items'][i]['items'].append({
                    'id': message_id,
                    'from_user': from_user,
                    't': 'gift',
                    'date': date,
                    'body': {
                        'photo': (
                            x['gift']['thumb_96'] or
                            x['gift']['thumb_256'] or
                            x['gift']['thumb_48']
                        ),
                        'message': x['gift'].get('message', '')
                    }
                })

            elif x['type'] == 'link':
                data['items'][i]['items'].append({
                    'id': message_id,
                    'from_user': from_user,
                    't': 'link',
                    'date': date,
                    'body': {
                        'text': body,
                        'url': x['link']['url']
                    }
                })

            elif x['type'] == 'call':
                data['items'][i]['items'].append({
                    'id': message_id,
                    'from_user': from_user,
                    't': 'call',
                    'date': date
                })

            elif x['type'] == 'doc':
                data['items'][i]['items'].append({
                    'id': message_id,
                    'from_user': from_user,
                    't': 'doc',
                    'date': date,
                    'body': {
                        'url': x['doc']['url'],
                        'title': x['doc']['title'],
                        'text': body
                    }
                })

            elif x['type'] == 'wall':
                data['items'][i]['items'].append({
                    'id': message_id,
                    'from_user': from_user,
                    't': 'wall',
                    'date': date,
                    'body': {
                        'url': 'https://vk.com/wall%s_%s' % (x['wall']['from_id'], x['wall']['id']),
                        'text': body,
                    }
                })
            elif x['type'] == 'wall_reply':
                data['items'][i]['items'].append({
                    'id': message_id,
                    'from_user': from_user,
                    't': 'wall_reply',
                    'date': date,
                    'body': {
                        'text': body,
                    }
                })
            elif x['type'] == 'market_album':
                data['items'][i]['items'].append({
                    'id': message_id,
                    'from_user': from_user,
                    't': 'market_album',
                    'date': date,
                    'body': {
                        'text': body
                    }
                })
            elif x['type'] == 'market':
                data['items'][i]['items'].append({
                    'id': message_id,
                    'from_user': from_user,
                    't': 'market',
                    'date': date,
                    'body': {
                        'text': body,
                        'photo': x['market'].get('thumb_photo', ''),
                        'title': x['market'].get('title', ''),
                        'url': 'https://vk.com/market%s_%s' % (x['market']['owner_id'], x['market']['id'])
                    }
                })
            elif x['type'] == 'podcast':
                data['items'][i]['items'].append({
                    'id': message_id,
                    'from_user': from_user,
                    't': 'podcast',
                    'date': date,
                    'body': {
                        'title': x['podcast']['artist']
                    }
                })
            else:
                print(message)
                input()

    elif message.get('fwd_messages', None):
        ms = []
        for j in range(len(message['fwd_messages'])):
            from_id = message['fwd_messages'][j]['user_id']

            if 1 == 2:
                from_user1 = user
            else:
                for member in persons:
                    if from_id == member['id']:
                        from_user1 = member
                        break
                    elif from_id == -member['id']:
                        from_user1 = member
                        break
                else:
                    extra_data = '&fields=photo_50&user_ids=%d' % from_id
                    response = send_request(http, 'users.get', token, extra_data)
                    if response.get('response', ''):
                        first_name = response['response'][0]['first_name']
                        last_name = response['response'][0]['last_name']
                        p = response['response'][0]['photo_50']
                    else:
                        extra_data = '&group_id=%d' % -from_id
                        response = send_request(http, 'groups.getById', token, extra_data)
                        if response.get('response', 0) != 0:
                            first_name = response['response'][0]['name']
                            last_name = ''
                            p = response['response'][0].get('photo_50', '') or response['response'][0].get('photo_100',
                                                                                                           '')
                        else:
                            first_name = 'UNDEFINED'
                            last_name = ''
                            p = ''

                    from_user1 = {
                        'url': 'https://vk.com/id%s' % from_id,
                        'first_name': first_name,
                        'last_name': last_name,
                        'id': from_id,
                        'photo': p
                    }

                    persons.append(from_user1)

            ms.append((get_cmess(message['fwd_messages'][j], user, user_id, persons, i, data, token, videos, message_id)[1], from_user1))

        data['items'][i]['items'].append({
            'id': message_id,
            'from_user': from_user,
            't': 'fwd',
            'date': date,
            'body': {
                'messages': ms,
                'text': body
            }
        })
    elif message.get('action', None):
        if message['action'] == 'chat_kick_user':
            action = '*Исключение пользователя из беседы*'
        elif message['action'] == 'chat_create':
            action = '*Создание беседы*'
        elif message['action'] == 'chat_invite_user':
            action = '*Приглашение в беседу*'
        elif message['action'] == 'chat_title_update':
            action = 'Название беседы изменено на "%s"' % message['action_text']
        elif message['action'] == 'chat_photo_remove':
            action = '*Фотография беседы была удалена*'
        elif message['action'] == 'chat_photo_update':
            action = '*Фотография беседы была обновлена*'
        else:
            action = ''
            print(message)
            input()
            #action = '*Приглашение в беседу*'
        data['items'][i]['items'].append({
            'id': message_id,
            'from_user': from_user,
            't': 'action',
            'date': date,
            'body': {
                'action': action
            }
        })
    else:
        data['items'][i]['items'].append({
            'id': message_id,
            'from_user': from_user,
            't': 'text',
            'date': date,
            'body': {
                'text': body
            }
        })

    tmp = data['items'][i]['items'][-1]
    if not message.get('from_id', None):
        del data['items'][i]['items'][-1]

    return message_id, tmp

