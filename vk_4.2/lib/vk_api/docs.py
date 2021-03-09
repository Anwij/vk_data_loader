from lib.vk_api.tools import send_request, transform_date


def get_docs(token):
    http = None
    extra_data = '&count=2000'
    response = send_request(http, 'docs.get', token, extra_data)
    docs_count = min(response['response']['count'], 200)
    docs = response['response']['items']

    data = {
        'count': docs_count,
        'items': []
    }

    for doc in docs:
        title = doc['title']
        url = doc['url']
        date = transform_date(doc['date'])

        data['items'].append({
            'title': title,
            'url': url,
            'date': date
        })

    return data
