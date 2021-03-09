import json
from time import gmtime, sleep
import requests

raw_url = 'https://api.vk.com/method/{method}?v=5.52&access_token={token}'


def send_request(http, method, token, extra_data=''):
	url = raw_url.format(method=method, token=token) + extra_data
	while True:
		response = requests.get(url).json()
		if not ('error' in response and response['error']['error_code'] == 6):
			break

	return response


def transform_date(date):
	months = [
		'янв',
		'фев',
		'мар',
		'апр',
		'май',
		'июн',
		'июл',
		'авг',
		'сен',
		'окт',
		'ноя',
		'дек'
	]

	d = gmtime(date)

	day = d.tm_mday
	month = d.tm_mon
	month = months[month - 1]
	year = d.tm_year
	hours = d.tm_hour
	minutes = d.tm_min
	minutes = '0%d' % minutes if minutes <= 9 else str(minutes)

	d = '%d %s %d в %d:%s' % (day, month, year, hours, minutes)
	return d


def get_name(name):
	name = ''.join([str(ord(x)) for x in name])
	return name