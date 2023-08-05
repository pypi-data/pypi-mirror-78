# TODO: Add base exception

class RequiredSettingNotFoundException(Exception):
    def __init__(self, param):
        self.msg = param

    def __str__(self):
        return "Required setting " + ">".join(self.msg) + " not found in the settings file."