# author:klx
# time:2022/5/8 -{TIME}
# function: MD5加密
#
from django.conf import settings
import hashlib
def md5(data_string):
    #SECRET_KEY为setting.py中默认的值
    obj = hashlib.md5(str(settings.SECRET_KEY).encode('utf8'))
    obj.update(str(data_string).encode('utf8'))
    return obj.hexdigest()