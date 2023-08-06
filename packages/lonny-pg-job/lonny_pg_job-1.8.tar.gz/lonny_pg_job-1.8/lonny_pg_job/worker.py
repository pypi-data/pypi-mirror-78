from functools import wraps
from contextlib import contextmanager
from pickle import dumps, loads
from base64 import b64decode, b64encode
from .logger import logger

class Job:
    def __init__(self, worker, slug, fn):
        self._worker = worker
        self._slug = slug
        self._fn = fn

    def __call__(self, *args, **kwargs):
        return self._worker._put_job(self._slug, args, kwargs)

    def now(self, *args, **kwargs):
        return self._fn(*args, **kwargs)

class Worker:
    def __init__(self, queue):
        self._queue = queue
        self._jobs = dict()
        self._on_schedule = list()
        self._on_error = list()

    @contextmanager
    def _get_job(self):
        with self._queue.get() as (payload, exists):
            if not exists:
                yield None
            decoded = b64decode(payload)
            yield loads(decoded)

    def _put_job(self, slug, args, kwargs):
        pickled = dumps([slug, args, kwargs])
        encoded = b64encode(pickled).decode("utf-8")
        self._queue.put(encoded)
        for hdlr in self._on_schedule:
            hdlr(slug, args, kwargs)

    def on_error(self, fn):
        self._on_error.append(fn)
        return fn

    def on_schedule(self, fn):
        self._on_schedule.append(fn)
        return fn

    def job(self, slug = None):
        def wrapper(fn):
            final_slug = ":".join([fn.__module__, fn.__name__]) if slug is None else slug
            self._jobs[final_slug] = fn
            return wraps(fn)(Job(final_slug, fn))
        return wrapper

    def _invoke(self, slug, args, kwargs):
        try:
            logger.info(f"Job: {slug} starting.")
            self._jobs[slug](*args, **kwargs)
            logger.info(f"Job: {slug} completed successfully.")
        except Exception as err:
            for hdlr in self._on_error:
                hdlr(slug, args, kwargs, err)
            logger.error(f"Job: {slug} failed.")
            logger.exception(err)

    def run_pending(self):
        while True:
            with self._get_job() as next_job:
                if next_job is None:
                    break
                slug, args, kwargs = next_job
                self._invoke(slug, args, kwargs)
        logger.info("No more jobs to run.")
