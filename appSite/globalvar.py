import warnings
from threading import Thread
import time


def threading_init(**kwargs):
    global _global_dict
    _global_dict = kwargs if kwargs else {}
    retry_delay = 0.2
    timeout = 60
    _global_dict['allowed_ips'] = []
    _global_dict['use_log'] = 0

    def _func():
        start_time = time.time()
        while True:
            try:
                from appSite.admin import AdminAllowHostModel, AdminSenderLogManagerModel
                break
            except:
                if time.time() - start_time >= timeout:
                    raise Exception('Cache Error')
                time.sleep(retry_delay)
        try:
            allowed_ips = AdminAllowHostModel.get_allowed_ips()
        except:
            allowed_ips = []
            warnings.warn('allowed_ips cache fail')
        set('allowed_ips', allowed_ips)

        try:
            use_log = AdminSenderLogManagerModel.get_use_log()
        except:
            use_log = 0
            warnings.warn('use_log cache fail')

        set('use_log', use_log)
        print('Cache Finish')

    Thread(target=_func).start()


def __init(**kwargs):
    global _global_dict
    _global_dict = kwargs if kwargs else {}
    _global_dict['allowed_ips'] = []
    _global_dict['use_log'] = 0


def set(key, value):
    _global_dict[key] = value


def get(key, default=None):
    if key in _global_dict.keys():
        return _global_dict[key]
    else:
        return default


def get_global():
    return _global_dict


def delete(key):
    try:
        del _global_dict[key]
    except:
        pass


def clear():
    _global_dict = {}
