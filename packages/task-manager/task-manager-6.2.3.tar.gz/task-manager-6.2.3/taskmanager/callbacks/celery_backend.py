# Copyright 2017 Biomedical Imaging Group Rotterdam, Departments of
# Medical Informatics and Radiology, Erasmus MC, Rotterdam, The Netherlands
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from taskmanager.callbacks import CALLBACK_BACKENDS, do_callback

try:
    from celery.signals import worker_process_init
    from celery import Celery, signals
    CELERY_IMPORTED = True
except ImportError:
    CELERY_IMPORTED = False

# If raven is used, try to setup raven to catch celery stuff
try:
    from raven.contrib.celery import register_signal, register_logger_signal
    from taskmanager import sentry
    client = sentry.client

    # register a custom filter to filter out duplicate logs
    register_logger_signal(client)

    # The register_signal function can also take an optional argument
    # `ignore_expected` which causes exception classes specified in Task.throws
    # to be ignored
    register_signal(client, ignore_expected=True)
    
except ImportError:
    pass


# Setup celery
class CeleryCallback:
    config_initialized = False

    if CELERY_IMPORTED:
        app = Celery('tasks')

        @staticmethod
        @app.task(bind=True, default_retry_delay=3600)
        def task_callback(self, url, content):
            try:
                do_callback(url, content)
            except Exception as exc:
                self.retry(exc=exc)

    def celery_callback(self, url, content, config):
        if not CELERY_IMPORTED:
            raise ImportError("Cannot use celery callback, celery python package appears not to be installed!")

        if not self.config_initialized:
            config = {
                'backend': config.get('TASKMAN_CELERY_BACKEND'),
                'broker': config.get('TASKMAN_CELERY_BROKER'),
            }

            self.app.conf.update(config)
            self.config_initialized = True

        self.task_callback.delay(url, content)


CALLBACK_BACKENDS['celery'] = CeleryCallback().celery_callback


if __name__ == '__main__':
    argv = [
        'worker',
        '--loglevel=DEBUG',
        '--loglevel=INFO',
    ]

    # crude fix for celery daemonized threads causing salt to fail
    # https://github.com/celery/celery/issues/1709
    @worker_process_init.connect
    def fix_multiprocessing(**kwargs):
        # don't be a daemon, so we can create new subprocesses
        from multiprocessing import current_process
        current_process().daemon = False

    @signals.setup_logging.connect
    def setup_celery_logging(**kwargs):
        pass

    app.worker_main(argv)

