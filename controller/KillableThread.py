import threading


class KillableThread(threading.Thread):
    def kill_to_tha_max(self):
        if not self._initialized:
            raise RuntimeError("Thread.__init__() not called")
        if not self._started.is_set():
            raise RuntimeError("cannot join thread before it is started")
        if self is threading.current_thread():
            raise RuntimeError("cannot join current thread")

        lock = self._tstate_lock
        if lock is not None:
            lock.release()

        self._is_stopped = True
        self._tstate_lock = None
        return
