import copy

from .errors import CodeAlreadyExistException


class StatusCode:
    available_codes = list()

    def __init__(self, code, message):
        if code in StatusCode.available_codes:
            raise CodeAlreadyExistException

        else:
            StatusCode.available_codes.append(code)

        self.code = code
        self.message = message

    def update_msg(self, new_msg):
        self.message = str(new_msg)

    def deep_copy(self, new_msg):
        status = copy.deepcopy(self)
        status.update_msg(new_msg)
        return status


from . import standard
