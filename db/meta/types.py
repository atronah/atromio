from sqlalchemy import Integer


class Money(Integer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)