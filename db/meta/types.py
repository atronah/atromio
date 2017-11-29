from sqlalchemy import Numeric


class Money(Numeric):
    def __init__(self, precision=16, scale=2, *args, **kvargs):
        super().__init__(precision, scale, *args, **kvargs)