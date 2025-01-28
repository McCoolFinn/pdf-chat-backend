class DatabaseRepository(object):
    def __init__(self, db_pool):
        self._pool = db_pool