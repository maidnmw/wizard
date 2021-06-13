import logging


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
s_handler = logging.StreamHandler()
s_handler.setLevel(logging.INFO)

f_handler = logging.FileHandler(filename='logs/error-logs.log')
f_handler.setLevel(logging.ERROR)
log.addHandler(s_handler)
log.addHandler(f_handler)


def res_error_parser(response, error_msg=''):
    error = response.get('error')
    if error:
        if error.get('error_code') == 6:
            log.info(f'{error_msg}\nERROR: {error}')
        else:
            log.error(f'{error_msg}\nERROR: {error}')
        return error
    return False
