from concurrent.futures.thread import ThreadPoolExecutor

DEFAULTEXECUTOR_MAX_WORKERS = 1


class DefaultExecutor(ThreadPoolExecutor):

    def __init__(self, max_workers: int = DEFAULTEXECUTOR_MAX_WORKERS, thread_name_prefix: str = "",
                 initializer=None, initargs: tuple = ()):
        super(DefaultExecutor, self).__init__(
            max_workers=max_workers,
            thread_name_prefix=thread_name_prefix,
            initializer=initializer,
            initargs=initargs
        )
