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

import os
from setuptools import setup

# Parse requirements file
with open('requirements.txt', 'r') as fh:
    _requires = fh.read().splitlines()

entry_points = {
    "console_scripts": [
        "taskmanager-db-init = taskmanager.__main__:db_init",
        "taskmanager-test-tasks = taskmanager.__main__:create_random_test_tasks",
        "taskmanager-test-taskgroup = taskmanager.__main__:create_random_test_taskgroup",
        "taskmanager-db-clean = taskmanager.__main__:db_clean",
        "taskmanager-db-reload = taskmanager.__main__:reload_data",
        "taskmanager-manager = taskmanager.__main__:flask_manager",
        #"taskmanager-run = taskmanager.__main__:run",
        #"taskmanager-run-gunicorn = taskmanager.__main__:run_gunicorn",
        "taskmanager-add-task = taskmanager.__main__:add_task",
        "taskmanager-add-template = taskmanager.__main__:add_template",
        "taskmanager-add-user = taskmanager.__main__:add_user",
        "taskmanager-config = taskmanager.__main__:config_from_file",
        "taskmanager-update-template = taskmanager.__main__:update_template",
    ],
}

VERSION = '6.2.3'
# When building something else than a release (tag) append the job id to the version.
if os.environ.get('CI_COMMIT_TAG'):
    pass
elif os.environ.get('CI_JOB_ID'):
    VERSION += f".{os.environ['CI_JOB_ID']}"

setup(
    name='task-manager',
    version=VERSION,
    author='H.C. Achterberg, M. Koek, A. Versteeg, H. Vrooman',
    author_email='h.achterberg@erasmusmc.nl, m.koek@erasmusmc.nl, a.versteeg@erasmusmc.nl, h.vrooman@erasmusmc.nl',
    packages=['taskmanager', 
              'taskmanager.api',
              'taskmanager.auth',
              'taskmanager.callbacks',
              'taskmanager.util',
             ],
    package_data={'taskmanager': ['templates/*', 'templates/**/*', 'static/*', 'static/**/*']},
    #package_data={'taskmanager.templates': ["**/*.html"], 'taskmanager': ['static/*.*', 'static/js/*.js']},
    url='https://gitlab.com/radiology/infrastructure/task-manager',
    license='Apache 2.0',
    description='The Task Manager is a server that tracks and dispenses tasks for clients to perform.',
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Education',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: System :: Logging',
        'Topic :: Utilities',
    ],
    install_requires=_requires,
    entry_points=entry_points,
)
