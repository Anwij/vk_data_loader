from lib.vk_api.info import get_info
import os


def get_user_token():
    for file_name in os.listdir(path=r'tokens'):
        try:
            for line in open(r'tokens/%s' % file_name, 'r', encoding='utf-8'):
                line = line.split(':')
                raw_token = ''
                try:
                    if len(line) > 2:
                        raw_token = line[2]
                    else:
                        raw_token = ''
                except:
                    pass
                token = raw_token.strip()
                if token:
                    info = get_info(token)
                    if info.get('error_code', ''):
                        continue
                    else:
                        return token
        except:
            pass
    return ''