
import multiprocessing as mp


class MultiprocessingWrapper:

    def __init__(self):
        self._pool = None
        self._m_queue = None
        self._manager = None

    @property
    def pool(self):
        if self._pool is None:
            self._pool = mp.Pool(self.__recomended_pool_size())
        return self._pool

    @property
    def managers_queue(self):
        if self._m_queue is None:
            self._m_queue = self.manager.Queue()
        return self._m_queue

    @property
    def manager(self):
        if self._manager is None:
            self._manager = mp.Manager()
        return self._manager

    def __recomended_pool_size(self):
        return mp.cpu_count() + 2


