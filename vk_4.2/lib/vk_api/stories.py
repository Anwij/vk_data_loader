from lib.vk_api.tools import send_request, transform_date


def get_stories(token):
    http = None
    response = send_request(http, 'stories.get', token)
    if not response.get('response', None):
        return {
        'count': 0,
        'items': []
    }
    stories_count = response['response']['count']
    stories = response['response']['items']

    data = {
        'count': stories_count,
        'items': []
    }

    for story in stories:
        story = story[0]
        date = transform_date(story['date'])
        story = story.get('photo', {})
        p = (
            story.get('photo_1280', '') or
            story.get('photo_807', '') or
            story.get('photo_604', '') or
            story.get('photo_256', '') or
            story.get('photo_130', '') or
            story.get('photo_75', '')
        )

        data['items'].append({
            'photo': p,
            'date': date
        })

    return data
