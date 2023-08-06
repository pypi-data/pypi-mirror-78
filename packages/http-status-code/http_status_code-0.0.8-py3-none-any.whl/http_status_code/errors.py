class CodeAlreadyExistException(Exception):
    def __init__(self):
        super().__init__('The required code is already used in the standard codes. Would you please choose another code.')
