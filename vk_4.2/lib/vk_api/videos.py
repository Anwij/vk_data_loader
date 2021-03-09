from lib.vk_api.tools import *


def get_videos(token):
    http = None
    extra_data = '&extended=1&count=200'
    response = send_request(http, 'video.get', token, extra_data)
    if not response.get('response', None):
        videos_count = 0
        videos = []
    else:
        videos_count = min(response['response']['count'], 200)
        videos = response['response']['items']

    data = {
        'count': videos_count,
        'items': []
    }

    for video in videos:
        title = video['title']
        url = video.get('player', '') or video.get('files', {}).get('external', '')
        photo = video.get('photo_320', '') or video.get('photo_130', '')

        data['items'].append({
            'title': title,
            'url': url,
            'photo': photo
        })

    return data
