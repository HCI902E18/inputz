import threading


class KillableThread(threading.Thread):
    def kill(self, consequences: bool = False) -> None:
        """
        This method will overwrite all thread locks and just kill the thread
        This code is NOT safety critical, but will kill thread waiting for iterator

        :param consequences: Bool to ensure that the user
                             understands the consequences of this method
        :return: None
        """
        if not consequences:
            raise RuntimeError("YOU NEED TO UNDERSTAND THE CONSEQUENCES OF THIS METHOD")
        if not self._initialized:
            raise RuntimeError("Thread.__init__() not called")
        if not self._started.is_set():
            raise RuntimeError("cannot join thread before it is started")
        if self is threading.current_thread():
            raise RuntimeError("cannot join current thread")

        lock = self._tstate_lock

        # THIS THREADING SHOULD NOT HOLD CRITICAL CODE
        if lock is not None:
            lock.release()

        self._is_stopped = True
        self._tstate_lock = None
        return
