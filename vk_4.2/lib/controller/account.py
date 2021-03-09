from lib.vk_api.info import get_info


class Account:
    def __init__(self, token: str):
        self.token = token
        info = get_info(token)
        self.name = '%s %s' % (info['first_name'], info['last_name'])
        self.id = info['id']