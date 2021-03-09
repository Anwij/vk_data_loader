from lib.vk_api.tools import *


def get_info(token):
	http = None
	response = send_request(http, 'account.getProfileInfo', token)

	if response.get('error', None):
		return {
			'error_code': response['error']['error_code'],
			'error_msg': response['error']['error_msg']
		}

	url = 'https://vk.com/id%d' % response['response']['id']
	first_name = response['response'].get('first_name', '')
	last_name = response['response'].get('last_name', '')
	home_town = response['response'].get('home_town', '')
	city = response['response'].get('city', {}).get('title', '')
	status = response['response'].get('status', '')

	r = response['response'].get('bdate', '')
	if r:
		day, month, year = r.split('.')
		if len(day) == 1: day = '0%s' % day
		if len(month) == 1: month = '0%s' % month
		bdate = '.'.join([day, month, year])
	else:
		bdate = ''

	country = response['response'].get('country', {}).get('title', '')
	phone = response['response'].get('phone', '')
	photo = response['response'].get('photo_200', '')
	user_id = response['response']['id']

	if response['response'].get('sex', None) == 1:
		sex = 'Женский'
	elif response['response'].get('sex', None) == 2:
		sex = 'Мужской'
	else:
		sex = ''

	relation = response['response'].get('relation', 0)

	if relation == 1: relation = 'Не женат' if sex == 'Мужской' else ('Не замужем' if sex == 'Женский' else 'Не женат/Не замужем')
	elif relation == 2: relation = 'Есть подруга' if sex == 'Мужской' else ('Есть друг' if sex == 'Женский' else 'Есть друг/Есть подруга')
	elif relation == 3: relation = 'Помолвлен' if sex == 'Мужской' else ('Помолвлена' if sex == 'Женский' else 'Помолвлен/Помолвлена')
	elif relation == 4: relation = 'Женат' if sex == 'Мужской' else ('Замужем' if sex == 'Женский' else 'Женат/Замужем')
	elif relation == 5: relation = 'Всё сложно'
	elif relation == 6: relation = 'В активном поиске'
	elif relation == 7: relation = 'Влюблен' if sex == 'Мужской' else ('Влюблена' if sex == 'Женский' else 'Влюблен/Влюблена')
	elif relation == 8: relation = 'В гражданском браке'
	else: relation = ''

	http = None
	extra_data = '&user_id=%d' % user_id
	response = send_request(http, 'messages.getLastActivity', token, extra_data)
	t = response['response'].get('time', '')

	data = {
		'first_name': first_name,
		'last_name': last_name,
		'url': url,
		'home_town': home_town,
		'city': city,
		'status': status,
		'bdate': bdate,
		'country': country,
		'phone': phone,
		'photo': photo,
		'id': user_id,
		'sex': sex,
		'relation': relation,
		'time': '' if not t else transform_date(t)
	}

	return data