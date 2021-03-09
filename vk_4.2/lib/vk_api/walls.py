from lib.vk_api.tools import send_request, transform_date


def get_walls(token):
    http = None
    response = send_request(http, 'wall.get', token)
    walls_count = response['response']['count']
    walls = response['response']['items']

    data = {
        'count': walls_count,
        'items': []
    }

    for wall in walls:
        url = 'https://vk.com/wall%s_%s' % (wall['from_id'], wall['id'])
        date = transform_date(wall['date'])

        data['items'].append({
            'url': url,
            'date': date
        })

    return data
