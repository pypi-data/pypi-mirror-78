class Block_Attack(Exception):
    def __init__(self, ErrorInfo):
        self.errorinfo = ErrorInfo

    def __str__(self):
        return self.errorinfo


class Suspect_Attack(Exception):
    def __init__(self, ErrorInfo):
        self.errorinfo = ErrorInfo

    def __str__(self):
        return self.errorinfo
