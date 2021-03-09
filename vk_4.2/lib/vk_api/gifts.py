from lib.vk_api.tools import send_request, transform_date


def get_gifts(token):
    http = None
    response = send_request(http, 'gifts.get', token)
    gifts_count = response['response']['count']
    gifts = response['response']['items']

    data = {
        'count': gifts_count,
        'items': []
    }

    for gift in gifts:
        photo = (
            gift['gift'].get('thumb_96', '') or
            gift['gift'].get('thumb_256', '') or
            gift['gift'].get('thumb_48', '')
        )
        from_url = 'https://vk.com/id%d' % gift['from_id']
        message = gift.get('message', '')
        date = transform_date(gift['date'])

        data['items'].append({
            'photo': photo,
            'from_url': from_url,
            'message': message,
            'date': date
        })

    return data
