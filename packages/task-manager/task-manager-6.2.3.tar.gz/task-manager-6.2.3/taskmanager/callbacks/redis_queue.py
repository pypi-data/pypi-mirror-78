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

from flask import current_app

try:
    from rq import Queue
    from redis import Redis
    REDIS_QUEUE_IMPORTED = True
except ImportError:
    REDIS_QUEUE_IMPORTED = False


class RedisCallback:
    # Get desired queue object
    def __init__(self):
        self._redis = None
        self._redis_queue = None
        self.config = None

    @property
    def redis_queue(self):
        if self._redis_queue is None:
            # Get config
            with current_app.app_context():
                redis_uri = self.config.get('TASKMAN_REDIS_QUEUE_URL', 'redis://localhost:6379')
                redis_queue_name = self.config.get('TASKMAN_REDIS_QUEUE_NAME', 'taskmanager_callbacks')

            # Create queue object
            self._redis = Redis.from_url(redis_uri)
            self._redis_queue = Queue(name=redis_queue_name, connection=self._redis, default_timeout=-1)

        return self._redis_queue

    def redis_queue_callback(self, url, content, config):
        if not REDIS_QUEUE_IMPORTED:
            raise ImportError("Cannot use redis queue callback, rq and/or redis python packages appears not to be installed!")

        if self.config is None:
            self.config = config

        self.redis_queue.enqueue(do_callback, url=url, content=content)


CALLBACK_BACKENDS['redis_queue'] = RedisCallback().redis_queue_callback
