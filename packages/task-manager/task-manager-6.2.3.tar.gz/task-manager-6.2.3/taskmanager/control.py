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
from typing import Dict, Optional, Sequence, Union

from . import exceptions, models
from .util.helpers import get_object_from_arg

db = models.db


def distribute_task(users=None, group=None, template=None):
    # Determine user list to select from
    if users is not None:
        pass
    elif group is not None:
        group = get_object_from_arg(group, models.Group, models.Group.groupname)
        users = group.users
    else:
        users = models.User.query.all()

    # Filter on users who have an assignment_weight higher than 0.
    users = [u for u in users if u.assignment_weight > 0]
    print(f"Found users: {users}")
    if not users:
        raise exceptions.InvalidArgumentsError('Did not find any users to distribute the task among!')

    # Construct a weight map for task assignment
    weight_map = {u.username: 0.0 for u in users}
    user_ids = [x.id for x in users]

    # Get the last tasks which where assigned to user(s). The task window is #users * 5.
    query = models.Task.query.filter(models.Task.users.any(models.User.id.in_(user_ids)) |
                                          models.Task.users_via_group.any(models.User.id.in_(user_ids)))

    # Optionally filter on template
    if template is not None:
        template = get_object_from_arg(template, models.TaskTemplate, models.TaskTemplate.label)
        query = query.filter(models.Task.template == template)

    query = query.order_by(
        models.Task.create_time.desc()
    ).limit(len(users) * 5)

    last_tasks = query.all()

    for previous_task in last_tasks:
        # If a task is assigned to multiple users, assign a part to each user.
        if len(previous_task.users) > 0:
            task_weight = 1.0 / len(previous_task.users)
            for user in previous_task.users:
                if user.username in weight_map:
                    # Weigh the task_weight with the user assignment weight
                    weight_map[user.username] += task_weight / user.assignment_weight

    print(f"Found user tasks weighting map: {weight_map}")

    if len(users) >= 1:
        user = min(list(weight_map.items()), key=lambda x: x[1])[0]  # Take username with minimum weight
        user = models.User.query.filter(models.User.username == user).one()

        print(f'Determined user {user} is de sjaak')
        return user
    else:
        print('WARNING: could not find proper user to assign task to')


def insert_task(content: Union[str, dict],
                project: str,
                callback_url: str,
                callback_content: str,
                template: str,
                generator_url: str,
                tags: Sequence[str]=None,
                users: Sequence[str]=None,
                groups: Sequence[str]=None,
                distribute_in_group: str=None,
                application_name: str=None,
                application_version: str=None,
                commit_to_db: bool=False) -> models.Task:
    """
    Insert a task into the database with all correct links to templates, tags,
    users and groups. Optionally distribute task in a group.

    :param content: string with task content
    :param project: project to assign the task to
    :param callback_url: url to call when task is done
    :param callback_content: content to sent to callback when task is done
    :param template: the task template
    :param generator_url: URL to the resource which created this task
    :param tags: list of tags
    :param users: list of users to which task is assigned to
    :param groups: list of groups to which task is assigned to
    :param distribute_in_group: distribute task in a group
    :param application_name: application for which the task is destined
    :param application_version: minimum application version required to open the task
    :param commit_to_db: commit to the database right away

    .. note::
        Distribute in group can only work if no users and groups are given

    .. warning::
        This will not commit the changes to the db by default, this is because callers 
        might want to make additional changes and have an atomic commit.
        The :param commit_to_db: parameter can be used to commit to the db directly.

    :return: newly created task object
    """
    # Get template, users and groups
    template = get_object_from_arg(template,
                                   models.TaskTemplate,
                                   models.TaskTemplate.label)

    if not isinstance(content, str):
        content = json.dumps(content)

    if users is not None:
        users = [get_object_from_arg(u, models.User, models.User.username) for u in users]

    if groups is not None:
        groups = [get_object_from_arg(g, models.Group, models.Group.groupname) for g in groups]

    # Create task object
    task = models.Task(project=project,
                       template=template,
                       content=content,
                       callback_url=callback_url,
                       callback_content=callback_content,
                       generator_url=generator_url,
                       application_name=application_name,
                       application_version=application_version)
    db.session.add(task)

    # Add tags (create if needed)
    if tags is not None:
        for tag in tags:
            tag_object = get_object_from_arg(tag, models.Tag, models.Tag.name, allow_none=True)

            if tag_object is None:
                tag_object = models.Tag(tag)
                db.session.add(tag_object)

            task.tags.append(tag_object)

    # Auto assign if not assigned to any user(s) or group(s)
    if users is None and groups is None:
        user = distribute_task(group=distribute_in_group)
        if user:
            task.users.append(user)
    else:
        if distribute_in_group is not None:
            raise exceptions.InvalidArgumentsError("Cannot specify group to distribute in and give specific "
                                                   "users/groups. Those options are mutually exclusive.")

        # Add the users and groups specified
        if users is not None:
            task.users = users

        if groups is not None:
            task.groups = groups

    if commit_to_db:
        db.session.commit()
        db.session.refresh(task)
    
    return task


def insert_taskgroup(label: str,
                     callback_url: str,
                     callback_content: str,
                     tasks: Optional[Sequence[Dict[str, Union[str, Sequence[str], None]]]]=None,
                     distribute_in_group: str=None,
                     distribute_method: str=None) -> models.TaskGroup:
    if tasks is None:
        tasks = []

    if distribute_method is None:
        distribute_method = 'same'

    valid_methods = ('unique', 'same')
    if distribute_method not in valid_methods:
        raise exceptions.InvalidArgumentsError(f'Distribute method should by one of {valid_methods}, found {distribute_method}')

    # Create all child tasks
    task_objects = []
    try:
        print(f'Getting users from group: {distribute_in_group}')
        group = get_object_from_arg(distribute_in_group, models.Group, models.Group.groupname)
        users = group.users
        print(f'Found users {users}')

        # Check if there is enough users to distribute the tasks to
        if distribute_method == 'unique':
            if len(tasks) > len(users):
                raise exceptions.InvalidArgumentsError('Not enough users to uniquely distribute all tasks in taskgroup!')

        new_user = distribute_task(users)
        print(f'New user: {new_user}')

        for task_info in tasks:
            # Update user(s)
            if distribute_in_group is not None:
                # Remove all task-specific user/group assignment
                task_info.pop('users', None)
                task_info.pop('groups', None)
                task_info.pop('distribute_in_group', None)

                # Set new user
                task_info['users'] = [new_user]

                # If needed, update user
                if distribute_method == 'unique':
                    users.remove(new_user)
                    new_user = distribute_task(users)

            # Create and save task
            task_objects.append(insert_task(**task_info))
    except exceptions.TaskManagerError as e:
        db.session.rollback()
        raise

    # Create final taskgroup
    taskgroup = models.TaskGroup(
        label=label,
        callback_url=callback_url,
        callback_content=callback_content,
        tasks=task_objects,
    )

    # Add object to db
    db.session.add(taskgroup)

    return taskgroup
