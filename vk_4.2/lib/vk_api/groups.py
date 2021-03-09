from lib.vk_api.tools import send_request
from lib.vk_api.info import get_info


def get_groups(token):
    http = None
    extra_data = '&extended=1&count=1000&fields=members_count'
    response = send_request(http, 'groups.get', token, extra_data)
    groups_count = min(response['response']['count'], 1000)
    groups = response['response']['items']

    data = {
        'count': groups_count,
        'items': []
    }
    a = 0
    for group in groups:
        name = group['name']
        photo = group.get('photo_50', '')
        url = 'https://vk.com/%s' % group['screen_name']

        data['items'].append({
            'name': name,
            'photo': photo,
            'url': url
        })

    return data
