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
        lock = self._tstate_lock

        # THIS THREADING SHOULD NOT HOLD CRITICAL CODE
        if lock is not None:
            lock.release()

        self._wait_for_tstate_lock(1)
