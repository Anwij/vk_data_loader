from lib.vk_api.tools import send_request


def get_black_list(token):
	http = None
	extra_data = '&count=200'
	response = send_request(http, 'account.getBanned', token, extra_data)
	black_list_count = min(response['response']['count'], 200)
	black_list = response['response']['items']

	data = {
		'count': black_list_count,
		'items': []
	}

	for person in black_list:
		first_name = person['first_name']
		last_name = person['last_name']
		url = 'https://vk.com/id%s' % person['id']

		data['items'].append({
			'id': person['id'],
			'first_name': first_name,
			'last_name': last_name,
			'url': url
		})

	return data
