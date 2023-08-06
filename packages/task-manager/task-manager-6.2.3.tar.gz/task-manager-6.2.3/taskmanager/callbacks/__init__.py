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

import json

import requests


def do_callback(url, content):
    """
    Execute the actual callback

    :param str url: URL to put to
    :param str content: String containing json payload to put
    """
    # Convert callback content to json
    content = json.loads(content)

    response = requests.put(url, json=content)
    print('PUT result: [{}] {}'.format(response.status_code, response.text))


def dispatch_callback(url, content, config):
    # Get the callback method from the config
    callback_method_name = config.get('TASKMAN_CALLBACK_METHOD')
    callback_function = CALLBACK_BACKENDS.get(callback_method_name, 'local')

    callback_function(url, content, config)


def local_callback(url, content, config):
    """
    Just run command locally
    """
    do_callback(url=url, content=content)


CALLBACK_BACKENDS = {
    'local': local_callback,
}

# These need to be at the end because they use do_callback and populate CALLBACK_BACKENDS
from . import celery_backend
from . import redis_queue
