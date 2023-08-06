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

from flask import Blueprint, abort, jsonify
from flask_restplus import Api, Resource, fields, inputs, reqparse
from flask_security import auth_required, current_user, http_auth_required, permissions_accepted, permissions_required
from flask_security.utils import hash_password

from . import RegisteredApi
from .. import exceptions
from .. import models
from .. import control
from .. import user_datastore
from ..fields import ObjectUrl, SubUrl
from ..util.helpers import get_object_from_arg

db = models.db

blueprint = Blueprint('api_v1', __name__)

authorization = {
    'basic_auth': {'type': 'basic'}
}

api = RegisteredApi(
    blueprint,
    version='1.0',
    title='TaskManager REST API',
    description='The TaskManager is for scheduling and managing tasks.',
    default_mediatype='application/json',
    authorization=authorization,
    security='basic_auth'
)


def json_type(data):
    """
    A simple type for request parser that just takes all json as is
    """
    return data


def int_or_str(value):
    return value if isinstance(value, int) else str(value)


def list_of_int_or_str(value):
    if not isinstance(value, list):
        value = list(value)
    return [int_or_str(x) for x in value]
    

def has_permission_any(*args):
    return any(current_user.has_permission(perm) for perm in args)


def has_permission_all(*args):
    return all(current_user.has_permission(perm) for perm in args)


tag_summary = api.model('TagSummary',
          {
              'uri': ObjectUrl('api_v1.tag', attribute='id'),
              'name': fields.String,
          }
)


tag_list_get = api.model("TagListGet", {
    'tags': fields.List(fields.Nested(tag_summary))
})


task_summary = api.model('TaskSummary',
          {
              'uri': ObjectUrl('api_v1.task', attribute='id'),
              'id': fields.String,
              'status': fields.String,
              'project': fields.String,
              'template': ObjectUrl('api_v1.task_template', attribute='template_id'),
              'tags': fields.List(fields.Nested(tag_summary))
          }
)


task_list_get = api.model('TaskListGet', {
    'tasks': fields.List(fields.Nested(task_summary))
})

task_get = api.model('TaskGet', {
    'uri': fields.Url('api_v1.task'),
    'project': fields.String,
    'template': ObjectUrl('api_v1.task_template', attribute='template_id'),
    'content': fields.String,
    'status': fields.String,
    'lock': SubUrl('api_v1.task', 'lock', attribute='id'),
    'tags': fields.List(ObjectUrl('api_v1.tag', attribute='id')),
    'callback_url': fields.String,
    'callback_content': fields.String,
    'generator_url': fields.String,
    'application_name': fields.String,
    'application_version': fields.String,
    'create_time': fields.DateTime,
    'update_time': fields.DateTime,
    'users': fields.List(ObjectUrl('api_v1.user', attribute='id')),
    'groups': fields.List(ObjectUrl('api_v1.group', attribute='id')),
    'users_via_group': fields.List(ObjectUrl('api_v1.user', attribute='id')),
})


task_post = api.model('TaskPost', {
    'project': fields.String,
    'template': fields.String,
    'content': fields.String,
    'tags': fields.List(ObjectUrl('api_v1.tag', attribute='id')),
    'callback_url': fields.String,
    'callback_content': fields.String,
    'generator_url': fields.String,
    'application_name': fields.String,
    'application_version': fields.String,
    'users': fields.List(ObjectUrl('api_v1.user', attribute='id')),
    'groups': fields.List(ObjectUrl('api_v1.group', attribute='id')),
    'distribute_in_group': fields.String,
})


task_put = api.model('TaskPut', {
    'project': fields.String,
    'template': fields.String,
    'content': fields.String,
    'status': fields.String,
    'callback_url': fields.String,
    'callback_content': fields.String,
    'generator_url': fields.String,
    'application_name': fields.String,
    'application_version': fields.String,
    'tags': fields.List(ObjectUrl('api_v1.tag', attribute='id')),
    'users': fields.List(ObjectUrl('api_v1.user', attribute='id')),
    'groups': fields.List(ObjectUrl('api_v1.group', attribute='id')),
})


@api.route('/tasks', endpoint='tasks')
class TaskListAPI(Resource):
    get_request_parser = reqparse.RequestParser()
    get_request_parser.add_argument('project', type=str, required=False, location='args', help="Filter on project name")
    get_request_parser.add_argument('template', type=str, required=False, location='args', help="Filter on template label")
    get_request_parser.add_argument('user', type=str, required=False, location='args', help="Filter on user by id or label")
    get_request_parser.add_argument('status', type=str, required=False, location='args', help="Filter on status.")
    get_request_parser.add_argument('tag', type=str, action='append', required=False, location='args', help="Tag name or list of tag names to filter on. When multiple tag args are given AND filter logic is applied.")
    get_request_parser.add_argument('application_name', type=str, required=False, location='args', help="Filter on application name")
    get_request_parser.add_argument('offset', type=int, required=False, location='args', help="Offset for pagination")
    get_request_parser.add_argument('limit', type=int, required=False, location='args', help="Maximum number of rows returned")

    post_request_parser = reqparse.RequestParser()
    post_request_parser.add_argument('project', type=str, required=True, location='json')
    post_request_parser.add_argument('template', type=str, required=True, location='json')
    post_request_parser.add_argument('content', type=json_type, required=True, location='json')
    post_request_parser.add_argument('callback_url', type=str, required=False, location='json')
    post_request_parser.add_argument('callback_content', type=str, required=False, location='json')
    post_request_parser.add_argument('generator_url', type=str, required=False, location='json')
    post_request_parser.add_argument('application_name', type=str, required=False, location='json')
    post_request_parser.add_argument('application_version', type=str, required=False, location='json')
    post_request_parser.add_argument('tags', type=list, required=False, location='json')
    post_request_parser.add_argument('users', type=list_of_int_or_str, required=False, location='json')
    post_request_parser.add_argument('groups', type=list_of_int_or_str, required=False, location='json')
    post_request_parser.add_argument('distribute_in_group', type=str, required=False, location='json')

    @http_auth_required
    @permissions_accepted('task_read', 'task_read_all')
    @api.marshal_with(task_list_get)
    @api.expect(get_request_parser)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find user or template')
    def get(self):
        args = self.get_request_parser.parse_args()
        user = args['user']
        project = args['project']
        status = args['status']
        template = args['template']
        tags = args['tag']
        application_name = args['application_name']
        offset = args['offset']
        limit = args['limit']

        # Allow retrieval of tasks by user or in general
        query = models.Task.query

        # If not task_real_all, only allow own tasks
        if not current_user.has_permission('task_read_all'):
            user = current_user
        # If tasks task_read_all allow to specify a user
        elif user is not None:
            user = get_object_from_arg(user,
                                       models.User,
                                       models.User.username,
                                       skip_id=True,
                                       allow_none=False)
        # Default to current user if no user was specified
        else:
            user = current_user

        # Query both tasks via user and via group
        tasks_via_user_query = query.filter(models.Task.users.contains(user))
        tasks_via_group_query = query.filter(models.Task.users_via_group.contains(user))
        query = tasks_via_user_query.union(tasks_via_group_query)

        if template is not None:
            template = get_object_from_arg(args['template'],
                                           models.TaskTemplate,
                                           models.TaskTemplate.label,
                                           allow_none=False)
            query = query.filter(models.Task.template == template)

        if project is not None:
            query = query.filter(models.Task.project == project)

        if status is not None:
            query = query.filter_by(_status=status)
        
        if tags is not None:
            for tag in tags:
                tag_object = models.Tag.query.filter_by(name = tag).one_or_none()
                if tag_object:
                    query = query.filter(models.Task.tags.contains(tag_object))

        if application_name is not None:
            query = query.filter(models.Task.application_name == application_name)

        if offset:
            query = query.offset(offset)

        if limit:
            query = query.limit(limit)

        tasks = query.all()

        return {'tasks': tasks}

    @http_auth_required
    @permissions_required('task_add')
    @api.marshal_with(task_get)
    @api.expect(task_post)
    @api.response(201, 'Created new task')
    @api.response(400, 'Invalid request: specified both users/groups and a distribute in group directive')
    @api.response(404, 'Could not find all users, groups or template')
    def post(self):
        args = self.post_request_parser.parse_args()

        try:
            task = control.insert_task(
                content=args['content'],
                project=args['project'],
                callback_url=args['callback_url'],
                callback_content=args['callback_content'],
                template=args['template'],
                generator_url=args['generator_url'],
                tags=args['tags'],
                users=args['users'],
                groups=args['groups'],
                distribute_in_group=args['distribute_in_group'],
                application_name=args['application_name'],
                application_version=args['application_version'],
            )
        except exceptions.TaskManagerError:
            db.session.rollback()
            raise

        # Commit changes to db
        print(f'Task.users {task.users}')
        print(f'Task.groups {task.groups}')
        db.session.commit()

        # Refresh the task object before returning
        db.session.refresh(task)
        return task, 201


@api.route('/tasks/<int:id>', endpoint='task')
class TaskAPI(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('project', type=str, required=False, location='json')
    request_parser.add_argument('template', type=str, required=False, location='json')
    request_parser.add_argument('content', type=json_type, required=False, location='json')
    request_parser.add_argument('status', type=str, required=False, location='json')
    request_parser.add_argument('callback_url', type=str, required=False, location='json')
    request_parser.add_argument('callback_content', type=str, required=False, location='json')
    request_parser.add_argument('generator_url', type=str, required=False, location='json')
    request_parser.add_argument('application_name', type=str, required=False, location='json')
    request_parser.add_argument('application_version', type=str, required=False, location='json')
    request_parser.add_argument('tags', type=list, required=False, location='json')
    request_parser.add_argument('users', type=list_of_int_or_str, required=False, location='json')
    request_parser.add_argument('groups', type=list_of_int_or_str, required=False, location='json')

    @http_auth_required
    @permissions_accepted('task_read', 'task_read_all')
    @api.marshal_with(task_get)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find selected task')
    def get(self, id):
        query = models.Task.query.filter(models.Task.id == id)

        if not current_user.has_permission('task_read_all'):
            tasks_via_user_query = query.filter(models.Task.users.contains(current_user))
            tasks_via_group_query = query.filter(models.Task.users_via_group.contains(current_user))
            query = tasks_via_user_query.union(tasks_via_group_query)
        task = query.one_or_none()

        if task is None:
            abort(404)

        return task

    @http_auth_required
    @permissions_accepted('task_update_status', 'task_update_status_all', 'task_update_user', 'task_update_all')
    @api.marshal_with(task_get)
    @api.expect(task_put)
    @api.response(200, 'Success')
    @api.response(403, 'You are not authorized to perform this operation')
    @api.response(404, 'Could not find selected task, user(s), group(s) or template')
    def put(self, id):
        query = models.Task.query.filter(models.Task.id == id)

        # Check if the current may change the status of all tasks or has task 
        # update super powers. If not limit to current_user assigned tasks only.
        if not has_permission_any('task_update_status_all', 'task_update_all'):
            tasks_via_user_query = query.filter(models.Task.users.contains(current_user))
            tasks_via_group_query = query.filter(models.Task.users_via_group.contains(current_user))
            query = tasks_via_user_query.union(tasks_via_group_query)
        task = query.one_or_none()
        
        if task is None:
            abort(404, 'Could not find selected task')

        args = self.request_parser.parse_args()

        if args['project'] is not None:
            if has_permission_any('task_update_all'):
                task.project = args['project']
            else:
                abort(403, "You are not authorized to update the project name")


        if args['template'] is not None:
            if has_permission_any('task_update_all'):
                try:
                    template = get_object_from_arg(args['template'],
                                                models.TaskTemplate,
                                                models.TaskTemplate.label)
                except exceptions.TaskManagerError as exception:
                    abort(exception.default_http_status, str(exception))

                task.template = template
            else:
                abort(403, "You are not authorized to update the template")


        if args['content'] is not None:
            if has_permission_any('task_update_all'):
                content = args['content']

                if not isinstance(content, str):
                    content = json.dumps(content)

                task.content = content
            else:
                abort(403, "You are not authorized to update the content")

        if args['status'] is not None:
            if has_permission_any('task_update_status', 'task_update_status_all', 'task_update_all'):
                task.status = args['status']
            else:
                abort(403, "You are not authorized to update the status")


        if args['callback_url'] is not None:
            if has_permission_any('task_update_all'):
                task.callback_url = args['callback_url']
            else:
                abort(403, "You are not authorized to update the callback url")


        if args['callback_content'] is not None:
            if has_permission_any('task_update_all'):
                task.callback_content = args['callback_content']
            else:
                abort(403, "You are not authorized to update the callback content")

        if args['generator_url'] is not None:
            if has_permission_any('task_update_all'):
                task.generator_url = args['generator_url']
            else:
                abort(403, "You are not authorized to update the generator url")

        if args['application_name'] is not None:
            if has_permission_any('task_update_all'):
                task.application_name = args['application_name']
            else:
                abort(403, "You are not authorized to update the application name")

        if args['application_version'] is not None:
            if has_permission_any('task_update_all'):
                task.application_version = args['application_version']
            else:
                abort(403, "You are not authorized to update the application version")

        # Add tags
        if args['tags'] is not None:
            if has_permission_any('task_update_all'):
                tags = []
                for tag in args['tags']:
                    if isinstance(tag, int):
                        tag_object = models.Tag.query.filter(models.Tag.id == tag).one_or_none()
                    else:
                        tag_object = models.Tag.query.filter(models.Tag.name == tag).one_or_none()

                    if tag_object is None:
                        print(f'Adding tag {tag}')
                        tag_object = models.Tag(tag)
                        db.session.add(tag_object)
                    else:
                        print(f'Reusing tag {tag}')

                    tags.append(tag_object)

                # Set the tags in one go (overwriting all old tags)
                task.tags = tags
            else:
                abort(403, "You are not authorized to update the tags")


        # Set users
        if args['users'] is not None:
            if has_permission_any('task_update_user', 'task_update_all'):
                users = []
                for user in args['users']:
                    if isinstance(user, int):
                        user_object = models.User.query.filter(models.User.id == user).one_or_none()
                    else:
                        user_object = models.User.query.filter(models.User.username == user).one_or_none()

                    if user_object is None:
                        abort(404, f"Could not find all users (user {user} not found)")

                    users.append(user_object)

                task.users = users
            else:
                abort(403, "You are not authorized to update the users")


        # Set groups
        if args['groups'] is not None:
            if has_permission_any('task_update_user', 'task_update_all'):
                groups = []
                for group in args['groups']:
                    if isinstance(group, int):
                        group_object = models.Group.query.filter(models.Group.id == group).one_or_none()
                    else:
                        group_object = models.Group.query.filter(models.Group.groupname == group).one_or_none()

                    if group_object is None:
                        abort(404, f"Could not find all groups (group {group} not found)")

                    groups.append(group_object)

                task.groups = groups
            else:
                abort(403, "You are not authorized to update the groups")

        db.session.commit()
        db.session.refresh(task)

        return task

    @http_auth_required
    @permissions_accepted('task_delete')
    @api.response(200, "Success")
    @api.response(404, "Could not find task")
    def delete(self, id):
        task = models.Task.query.filter(models.Task.id == id).one_or_none()

        if task is None:
            abort(404)
        
        db.session.delete(task)
        db.session.commit()


taskgroup = api.model(
    'TaskGroupGet',
    {
        'url': ObjectUrl('api_v1.taskgroup', attribute='id'),
        'id': fields.String,
        'label': fields.String,
        'status': fields.String,
        'callback_url': fields.String,
        'callback_content': fields.String,
        'tasks': fields.List(
            fields.Nested(task_summary)
        )
    }
)

taskgroup_list_post = api.model(
    'TaskGroupPost',
    {
        'label': fields.String,
        'callback_url': fields.String,
        'callback_content': fields.String,
        'distribute_in_group': fields.String,
        'distribute_method': fields.String,
        'tasks': fields.List(
            fields.Nested(task_post)
        )
    }
)

taskgroup_list_get = api.model('TaskGroupListGet', {
    'taskgroups': fields.List(
        fields.Nested(
            api.model('TaskgroupSummary',
                      {
                          'url': ObjectUrl('api_v1.taskgroup', attribute='id'),
                          'id': fields.String,
                          'label': fields.String,
                          'status': fields.String,
                      }
            )
        )
    )
})


@api.route('/taskgroups', endpoint='taskgroups')
class TaskGroupListAPI(Resource):
    get_request_parser = reqparse.RequestParser()
    get_request_parser.add_argument('status', type=str, required=False, location='args')

    post_request_parser = reqparse.RequestParser()
    post_request_parser.add_argument('label', type=str, required=True, location='json')
    post_request_parser.add_argument('callback_url', type=str, required=True, location='json')
    post_request_parser.add_argument('callback_content', type=str, required=True, location='json')
    post_request_parser.add_argument('tasks', type=list, required=True, location='json')
    post_request_parser.add_argument('distribute_in_group', type=str, required=False, location='json')
    post_request_parser.add_argument('distribute_method', type=str, required=False, location='json')

    @http_auth_required
    @permissions_accepted('task_read', 'task_read_all')
    @api.marshal_with(taskgroup_list_get)
    @api.expect(get_request_parser)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find user or template')
    def get(self):
        args = self.get_request_parser.parse_args()
        status = args['status']

        taskgroups = models.TaskGroup.query.all()

        if status is not None:
            taskgroups = [x for x in taskgroups if x.status == status]

        return {'taskgroups': taskgroups}

    @http_auth_required
    @permissions_accepted('task_add', 'task_update_all')
    @api.marshal_with(taskgroup)
    @api.expect(taskgroup_list_post)
    @api.response(201, 'Created')
    @api.response(404, 'Could not find a required resource')
    def post(self):
        args = self.post_request_parser.parse_args()
        label = args['label']
        callback_url = args['callback_url']
        callback_content = args['callback_content']
        distribute_in_group = args['distribute_in_group']
        distribute_method = args['distribute_method']
        tasks = args['tasks']

        taskgroup = control.insert_taskgroup(label=label,
                                             callback_url=callback_url,
                                             callback_content=callback_content,
                                             distribute_in_group=distribute_in_group,
                                             distribute_method=distribute_method,
                                             tasks=tasks)
        # Commit and return
        db.session.commit()
        db.session.refresh(taskgroup)
        return taskgroup, 201


taskgroup_put = api.model(
    'TaskGroupGet',
    {
        'label': fields.String,
        'callback_url': fields.String,
        'callback_content': fields.String,
        'tasks': fields.List(fields.Integer)
    }
)

@api.route('/taskgroups/<id>', endpoint='taskgroup')
class TaskGroupAPI(Resource):
    put_request_parser = reqparse.RequestParser()
    put_request_parser.add_argument('label', type=str, required=False, location='json')
    put_request_parser.add_argument('callback_url', type=str, required=False, location='json')
    put_request_parser.add_argument('callback_content', type=str, required=False, location='json')
    put_request_parser.add_argument('tasks', type=list, required=False, location='json')

    @http_auth_required
    @permissions_accepted('task_read', 'task_read_all')
    @api.marshal_with(taskgroup)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find selected taskgroup')
    def get(self, id):
        return get_object_from_arg(id, models.TaskGroup, models.TaskGroup.label)

    @http_auth_required
    @permissions_accepted('task_add', 'task_update_all')
    @api.marshal_with(taskgroup)
    @api.expect(taskgroup_put)
    @api.response(200, 'Success')
    @api.response(404, 'Taskgroup or child task not found')
    def put(self, id):
        args = self.put_request_parser.parse_args()
        taskgroup = get_object_from_arg(id, models.TaskGroup, models.TaskGroup.label)

        # Unpack arguments
        label = args['label']
        callback_url = args['callback_url']
        callback_content = args['callback_content']
        tasks = args['tasks']

        if label is not None:
            taskgroup.label = label

        if callback_url is not None:
            taskgroup.callback_url = callback_url

        if callback_content is not None:
            taskgroup.callback_content = callback_content

        if tasks is not None:
            tasks = [get_object_from_arg(x, models.Task) for x in tasks]
            taskgroup.tasks = tasks

        db.session.commit()
        db.session.refresh(taskgroup)
        return taskgroup


def user_type(value):
    if value is None:
        return None
    elif isinstance(value, int):
        return value
    else:
        return str(value)


lock_get = api.model('LockGet', {
    'lock': ObjectUrl('api_v1.user', object_id='id'),
    'username': fields.String,
    'error': fields.String
})


lock_put = api.model('LockPut', {
    'lock': ObjectUrl('api_v1.user', object_id='id'),
})


@api.route('/tasks/<int:id>/lock', endpoint='lock')
class LockAPI(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('lock', type=user_type, required=False, location='json')

    @http_auth_required
    @permissions_accepted('task_read', 'task_read_all')
    @api.marshal_with(lock_get)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find selected task')
    def get(self, id):
        query = models.Task.query.filter(models.Task.id == id)
        if not has_permission_any('task_read_all'):
            tasks_via_user_query = query.filter(models.Task.users.contains(current_user))
            tasks_via_group_query = query.filter(models.Task.users_via_group.contains(current_user))
            query = tasks_via_user_query.union(tasks_via_group_query)
        task = query.one_or_none()

        if task is None:
            abort(404)

        if task.lock is None:
            return jsonify({'lock': None, 'error': None})

        result = {
            "lock": task.lock,
            "username": task.lock.username if task.lock is not None else None,
            "error": None
        }
        return result

    @http_auth_required
    @permissions_accepted('task_read', 'task_update_lock_all', 'task_update_all')
    @api.marshal_with(lock_get)
    @api.response(200, 'Success')
    @api.response(403, 'You are not authorized to release the lock of another user')
    @api.response(404, 'Could not find selected task or user')
    def delete(self, id):
        query = models.Task.query.filter(models.Task.id == id)
        if not has_permission_any('task_update_lock_all', 'task_update_all'):
            tasks_via_user_query = query.filter(models.Task.users.contains(current_user))
            tasks_via_group_query = query.filter(models.Task.users_via_group.contains(current_user))
            query = tasks_via_user_query.union(tasks_via_group_query)
        task = query.one_or_none()

        if task is None:
            result = {"error": f'Could not find the specified task lock (task {id} does not exist)!',
                      "username": None,
                      "lock": None}
            return result, 404

        if task.lock is not None and task.lock != current_user and not has_permission_any('task_update_lock_all', 'task_update_all'):
            # If the task is locked and not by you and you are not authorized to update all locks, throw 403.
            result = {"error": 'You are not authorized to release the lock of a task, assigned to someone else!',
                        "username": None, "lock": None}
            return result, 403
        else:
            # You are authorized to release this lock.
            task.lock = None
            result = {"lock": None, "username": None, "error": None}
            db.session.commit()
            return result
    
    @http_auth_required
    @permissions_accepted('task_read', 'task_update_lock_all', 'task_update_all')
    @api.marshal_with(lock_get)
    @api.expect(lock_put)
    @api.response(200, 'Success')
    @api.response(403, 'You are not authorized to update the lock this task to someone else')
    @api.response(404, 'Could not find selected task or user')
    @api.response(409, 'Task already locked by other user')
    def put(self, id):
        query = models.Task.query.filter(models.Task.id == id)
        if not has_permission_any('task_update_lock_all', 'task_update_all'):
            tasks_via_user_query = query.filter(models.Task.users.contains(current_user))
            tasks_via_group_query = query.filter(models.Task.users_via_group.contains(current_user))
            query = tasks_via_user_query.union(tasks_via_group_query)
        task = query.one_or_none()

        if task is None:
            result = {"error": f'Could not find the specified task lock (task {id} does not exist)!',
                      "username": None,
                      "lock": None}
            return result, 404

        args = self.request_parser.parse_args()
        if args['lock']:
            # Lock is given, now try to set the lock
            lock = args['lock']
            if isinstance(lock, int):
                user = models.User.query.filter(models.User.id == lock).one_or_none()
            else:
                user = models.User.query.filter(models.User.username == lock).one_or_none()

            if user is None:
                result = {"lock": task.lock,
                          "username": task.lock.username if task.lock is not None else None,
                          "error": f'Could not find the specified user to update lock to (user {lock} does not exist)!'}
                return result, 404

            if task.lock is not None and task.lock != user:
                if has_permission_any('task_update_lock_all', 'task_update_all'):
                    # This user has the right permission to overwrite any lock, so proceed.
                    task.lock = user
                else:
                    # This user is not authorized to overwrite a lock from another user.
                    result = {"lock": task.lock,
                              "username": task.lock.username if task.lock is not None else None,
                              "error": 'Task already locked!'}
                    return result, 409

            if has_permission_any('task_update_lock_all', 'task_update_all'):
                # When a user has a task_update_lock_all and/or task_update_all permission, the lock
                # may be (over)written at all times to the specified user.
                task.lock = user
            else:
                # When a user does not have an *_all permission, the user may still lock a task of itself.
                if user == current_user:
                    # This is allowed! A user can lock its own to task itself.
                    task.lock = user
                else:
                    result = {"lock": task.lock,
                              "username": task.lock.username if task.lock is not None else None,
                              "error": 'You may not lock this task to another user'}
                    return result, 403

        else:
            # No lock is given in the arguments, try to lock this task to the requesting user.
            if task.lock is not None and task.lock != current_user:
                # A lock already has been set 
                result = {"lock": task.lock,
                          "username": task.lock.username if task.lock is not None else None,
                          "error": 'Task already locked!'}
                return result, 409
            else:
                task.lock = current_user

        # Commit all changes to the database 
        db.session.commit()
        db.session.refresh(task)

        result = {
            "lock": task.lock,
            "username": task.lock.username if task.lock is not None else None,
            "error": None
        }
        return result


task_template_get = api.model('TaskTemplateGet', {
    'uri': ObjectUrl('api_v1.task_template', attribute='label'),
    'label': fields.String,
    'content': fields.String,
})


task_template_post = api.model('TaskTemplatePost', {
    'label': fields.String,
    'content': fields.Raw,
})


task_template_list_get = api.model('TaskTemplateListGet', {
    'task_templates': fields.List(ObjectUrl('api_v1.task_template', attribute='label'))
})


@api.route('/task_templates', endpoint='task_templates')
class TaskTemplateListAPI(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('label', type=str, required=True, location='json')
    request_parser.add_argument('content', type=json_type, required=True, location='json')

    @http_auth_required
    @permissions_accepted('task_read', 'task_read_all')
    @api.marshal_with(task_template_list_get)
    def get(self):
        task_templates = models.TaskTemplate.query.all()
        return {'task_templates': task_templates}

    @http_auth_required
    @permissions_accepted('template_add')
    @api.marshal_with(task_template_get)
    @api.expect(task_template_post)
    @api.response(201, "Create task template")
    def post(self):
        arguments = self.request_parser.parse_args()
        label = arguments['label']
        content = arguments['content']

        if not isinstance(content, str):
            content = json.dumps(content)

        task_template = models.TaskTemplate(label=label, content=content)
        db.session.add(task_template)
        db.session.commit()

        # Refresh the task object before returning
        db.session.refresh(task_template)
        return task_template, 201


@api.route('/task_templates/<id>', endpoint='task_template')
class TaskTemplateAPI(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('label', type=str, required=False, location='json')
    request_parser.add_argument('content', type=json_type, required=False, location='json')

    @http_auth_required
    @permissions_accepted('task_read', 'task_read_all')
    @api.marshal_with(task_template_get)
    @api.response(200, "Success")
    @api.response(404, "Could not find task template")
    def get(self, id):
        task_template = get_object_from_arg(id, models.TaskTemplate, models.TaskTemplate.label)

        if task_template is None:
            abort(404)

        return task_template

    @http_auth_required
    @permissions_accepted('template_update')
    @api.marshal_with(task_template_get)
    @api.response(200, "Success")
    @api.response(404, "Could not find task template")
    @api.expect(task_template_post)
    def put(self, id):
        task_template = get_object_from_arg(id, models.TaskTemplate, models.TaskTemplate.label)
        if task_template is None:
            abort(404)

        args = self.request_parser.parse_args()

        if args['label'] is not None:
            task_template.label = args['label']

        if args['content'] is not None:
            content = args['content']
            print(f'Found content: [{type(content).__name__}] {content}')

            if not isinstance(content, str):
                content = json.dumps(content)

            task_template.content = content

        db.session.commit()
        db.session.refresh(task_template)
        return task_template

    @http_auth_required
    @permissions_accepted('template_delete')
    @api.response(200, "Success")
    @api.response(404, "Could not find task template")
    def delete(self, id):
        task_template = get_object_from_arg(id, models.TaskTemplate, models.TaskTemplate.label)
        if task_template is None:
            abort(404)

        db.session.delete(task_template)
        db.session.commit()


tag_get = api.model("TagGet",
    {
        'name': fields.String,
        'uri': fields.Url('api_v1.tag'),
        'tasks': SubUrl('api_v1.tag', 'tasks', attribute='id')
    }
)


tag_put = api.model("TagPut", {
    'name': fields.String,
})


@api.route('/tags', endpoint='tags')
class TagListAPI(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('name', type=str, required=True, location='json')

    @http_auth_required
    @api.marshal_with(tag_list_get)
    def get(self):
        tags = models.Tag.query.all()
        return {'tags': tags}

    @http_auth_required
    @permissions_accepted('tag_add')
    @api.marshal_with(tag_get)
    @api.expect(tag_put)
    @api.response(201, "Created tag")
    def post(self):
        tag = models.Tag(**self.request_parser.parse_args())
        db.session.add(tag)
        db.session.commit()
        db.session.refresh(tag)
        return tag, 201


@api.route('/tags/<int:id>', endpoint='tag')
class TagAPI(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('name', type=str, required=False, location='json')

    @http_auth_required
    @api.marshal_with(tag_get)
    @api.response(200, "Success")
    @api.response(404, "Could not find tag")
    def get(self, id):
        tag = models.Tag.query.filter(models.Tag.id == id).one_or_none()
        if tag is None:
            abort(404)
        return tag

    @http_auth_required
    @permissions_accepted('tag_update')
    @api.marshal_with(tag_get)
    @api.expect(tag_put)
    @api.response(200, "Success")
    @api.response(404, "Could not find tag")
    def put(self, id):
        tag = models.Tag.query.filter(models.Tag.id == id).one_or_none()
        if tag is None:
            abort(404)

        args = self.request_parser.parse_args()

        if args['name'] is not None:
            tag.project = args['name']

        db.session.commit()
        db.session.refresh(tag)
        return tag

    @http_auth_required
    @permissions_accepted('tag_delete')
    @api.response(200, "Success")
    @api.response(404, "Could not find tag")
    def delete(self, id):
        tag = models.Tag.query.filter(models.Tag.id == id).one_or_none()
        if tag is None:
            abort(404)

        db.session.delete(tag)
        db.session.commit()


@api.route('/tags/<int:id>/tasks', endpoint='tagtasks')
class TagTaskListAPI(Resource):
    @http_auth_required
    @permissions_accepted('task_read', 'task_read_all')
    @api.marshal_with(task_list_get)
    @api.response(200, "Succes")
    @api.response(404, "Could not find tag")
    def get(self, id):
        tag = models.Tag.query.filter(models.Tag.id == id).one_or_none()

        if tag is None:
            abort(404)
        
        return {'tasks': tag.tasks}


user_list_get = api.model("UserListGet", {
    'users': fields.List(ObjectUrl('api_v1.user', attribute='id'))
})


user_get = api.model("UserGet", {
    'username': fields.String,
    'uri': fields.Url('api_v1.user'),
    'name': fields.String,
    'active': fields.Boolean,
    'email': fields.String,
    'create_time': fields.DateTime,
    'assignment_weight': fields.Float,
    'tasks': SubUrl('api_v1.user', 'tasks', attribute='id'),
    'groups': SubUrl('api_v1.user', 'groups', attribute='id'),
})


user_put = api.model("UserPut", {
    'username': fields.String,
    'name': fields.String,
    'active': fields.Boolean,
    'email': fields.String,
    'password': fields.String,
    'assignment_weight': fields.Float,
})


@api.route('/users', endpoint='users')
class UserListAPI(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('username', type=str, required=True, location='json')
    request_parser.add_argument('password', type=str, required=True, location='json')
    request_parser.add_argument('name', type=str, required=True, location='json')
    request_parser.add_argument('email', type=str, required=True, location='json')
    request_parser.add_argument('active', type=bool, required=False, default=True, location='json')
    request_parser.add_argument('assignment_weight', type=float, required=False, default=1.0, location='json')

    @http_auth_required
    @permissions_accepted('user_read_all')
    @api.marshal_with(user_list_get)
    @api.response(200, "Success")
    def get(self):
        users = models.User.query.all()
        return {'users': users}

    @http_auth_required
    @permissions_accepted('user_add')
    @api.marshal_with(user_get)
    @api.expect(user_put)
    @api.response(201, "Created user")
    def post(self):
        args = self.request_parser.parse_args()
        args['password'] = hash_password(args['password'])
        user = user_datastore.create_user(**args)
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user, 201


@api.route('/users/<id>', endpoint='user')
class UserAPI(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('username', type=str, required=False, location='json')
    request_parser.add_argument('password', type=str, required=False, location='json')
    request_parser.add_argument('name', type=str, required=False, location='json')
    request_parser.add_argument('email', type=str, required=False, location='json')
    request_parser.add_argument('assignment_weight', type=float, required=False, location='json')
    request_parser.add_argument('active', type=bool, required=False, location='json')

    @http_auth_required
    @permissions_accepted('user_read', 'user_read_all')
    @api.marshal_with(user_get)
    @api.response(200, "Success")
    @api.response(403, "You are not authorized to get this information")
    @api.response(404, "Could not find user")
    def get(self, id):
        user = models.User.query.filter(models.User.id == id).one_or_none()

        if not has_permission_any('user_read_all'):
            if user != current_user:
                abort(403, "You are not authorized to get this information")

        if user is None:
            abort(404)

        return user

    @http_auth_required
    @permissions_accepted('user_update_assignment_weight', 'user_update_all')
    @api.marshal_with(user_get)
    @api.expect(user_put)
    @api.response(200, "Success")
    @api.response(403, "You are not authorized to perform this operation")
    @api.response(404, "Could not find user")
    def put(self, id):
        user = models.User.query.filter(models.User.id == id).one_or_none()
        if user is None:
            abort(404)

        args = self.request_parser.parse_args()

        if args['username'] is not None:
            if has_permission_all('user_update_all'):
                user.username = args['username']
            else:
                abort(403, "You are not authorized to change the username")

        if args['password'] is not None:
            if has_permission_all('user_update_all'):
                user.password = args['password']
            else:
                abort(403, "You are not authorized to change the password")

        if args['name'] is not None:
            if has_permission_all('user_update_all'):
                user.name = args['name']
            else:
                abort(403, "You are not authorized to change the name")
        
        if args['active'] is not None:
            if has_permission_all('user_update_all'):
                user.active = args['active']
            else:
                abort(403, "You are not authorized to change the activeness")

        if args['email'] is not None:
            if has_permission_all('user_update_all'):
                user.email = args['email']
            else:
                abort(403, "You are not authorized to change the email")


        if args['assignment_weight'] is not None:
            user.assignment_weight = args['assignment_weight']

        db.session.commit()
        db.session.refresh(user)

        return user

    @http_auth_required
    @permissions_accepted('user_delete')
    @api.response(200, "Success")
    @api.response(404, "Could not find user")
    def delete(self, id):
        user = models.User.query.filter(models.User.id == id).one_or_none()

        if user is None:
            abort(404)

        user.active = False
        db.session.commit()


role_get = api.model("RoleGet", {
    'name': fields.String, 
    'description': fields.String,
    'update_datetime': fields.DateTime,
    'permissions': fields.List(fields.String)
})


role_list_get = api.model("RoleListGet", {
    'roles': fields.List(ObjectUrl('api_v1.role', attribute='id'))
})


@api.route('/roles', endpoint='roles')
class RoleListAPI(Resource):
    @http_auth_required
    @permissions_accepted('roles_manage')
    @api.marshal_with(role_list_get)
    @api.response(200, "Success")
    def get(self):
        roles = models.Role.query.all()
        return {"roles": roles}


@api.route('/roles/<id>', endpoint='role')
class RoleApi(Resource):
    @http_auth_required
    @permissions_accepted('roles_manage')
    @api.marshal_with(role_get)
    @api.response(200, "Success")
    @api.response(404, "Could not find role")
    def get(self, id):
        role = models.Role.query.filter_by(id = id).one_or_none()
        if role is None:
            abort(404)
        return {'name': role.name,
                'description': role.description,
                'update_datetime': role.update_datetime,
                'permissions': role.get_permissions()}


@api.route('/users/<user_id>/roles/<role_id>', endpoint='userrole')
class UserRoleAPI(Resource):
    @auth_required('session', 'basic')
    @permissions_accepted('roles_manage')
    @api.response(200, "Success")
    @api.response(404, "User or Role not found")
    def put(self, user_id, role_id):
        role = get_object_from_arg(role_id, models.Role, models.Role.name)
        user = get_object_from_arg(user_id, models.User, models.User.username)

        if user not in role.users:
            role.users.append(user)
            db.session.commit()
            db.session.refresh(role)

        return {"role": role.id, "user": user.id, "has_role": user in role.users}

    @auth_required('session', 'basic')
    @permissions_accepted('roles_manage')
    @api.response(200, "Success")
    @api.response(404, "User or Role not found")
    def delete(self, user_id, role_id):
        role = get_object_from_arg(role_id, models.Role, models.Role.name)
        user = get_object_from_arg(user_id, models.User, models.User.username)

        user.roles = [x for x in user.roles if x != role]
        db.session.commit()
        db.session.refresh(user)
        db.session.refresh(role)

        return {"role": role.id, "user": user.id, "has_role": user in role.users}


@api.route('/users/<id>/tasks', endpoint='usertasks')
class UserTaskListAPI(Resource):
    @http_auth_required
    @permissions_accepted('task_read', 'task_read_all', 'user_read', 'user_read_all')
    @api.marshal_with(task_list_get)
    @api.response(200, "Success")
    @api.response(403, "You are not authorized to get this information")
    @api.response(404, "Could not find user")
    def get(self, id):
        user = models.User.query.filter(models.User.id == id).one_or_none()

        if user is None:
            abort(404)

        if not has_permission_any('task_read_all', 'user_read_all'):
            if user != current_user:
                abort(403)


        return {'tasks': user.tasks}


group_list_get = api.model("GroupListGet", {
    'groups': fields.List(ObjectUrl('api_v1.group', attribute='id'))
})


group_get = api.model("GroupGet", {
    'groupname': fields.String,
    'uri': fields.Url('api_v1.group'),
    'name': fields.String,
    'create_time': fields.DateTime,
    'tasks': SubUrl('api_v1.group', 'tasks', attribute='id'),
    'users': SubUrl('api_v1.group', 'users', attribute='id'),
})


group_put = api.model("GroupPut", {
    'groupname': fields.String,
    'name': fields.String,
})


@api.route('/users/<id>/groups', endpoint='usergroups')
class UserGroupListAPI(Resource):
    @http_auth_required
    @permissions_accepted('user_read', 'user_read_all')
    @api.marshal_with(group_list_get)
    @api.response(200, "Success")
    @api.response(403, "You are not authorized to get this information")
    @api.response(404, "User not found")
    def get(self, id):
        user = models.User.query.filter(models.User.id == id).one_or_none()

        if not has_permission_any('user_read_all'):
            if user != current_user:
                abort(403, "You are not authorized to get this information")

        if user is None:
            abort(404)
        
        return {'groups': user.groups}


@api.route('/groups', endpoint='groups')
class GroupListAPI(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('groupname', type=str, required=True, location='json')
    request_parser.add_argument('name', type=str, required=False, location='json')

    @http_auth_required
    @permissions_accepted('group_read_all')
    @api.marshal_with(group_list_get)
    def get(self):
        groups = models.Group.query.all()
        return {"groups": groups}

    @http_auth_required
    @permissions_accepted('group_add')
    @api.marshal_with(group_get)
    @api.expect(group_put)
    @api.response(201, "Created group")
    def post(self):
        args = self.request_parser.parse_args()
        if args['name'] is None:
            args['name'] = args['groupname']

        group = models.Group(**args)
        db.session.add(group)
        db.session.commit()
        db.session.refresh(group)
        return group, 201


@api.route('/groups/<id>', endpoint='group')
class GroupAPI(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('groupname', type=str, required=False, location='json')
    request_parser.add_argument('name', type=str, required=False, location='json')

    @http_auth_required
    @permissions_accepted('group_read', 'group_read_all')
    @api.marshal_with(group_get)
    @api.response(200, "Success")
    @api.response(404, "Could not find group")
    def get(self, id):
        group = models.Group.query.filter(models.Group.id == id).one_or_none()

        if group is None:
            abort(404)

        if not has_permission_all('group_read_all'):
            if group not in current_user.groups:
                abort(403)

        return group

    @http_auth_required
    @permissions_accepted('group_update')
    @api.marshal_with(group_get)
    @api.expect(group_put)
    @api.response(200, "Success")
    @api.response(404, "Could not find group")
    def put(self, id):
        group = models.Group.query.filter(models.Group.id == id).one_or_none()
        if group is None:
            abort(404)

        args = self.request_parser.parse_args()

        if args['groupname'] is not None:
            group.groupname = args['groupname']

        if args['name'] is not None:
            group.name = args['name']

        db.session.commit()
        db.session.refresh(group)

        return group
    
    @http_auth_required
    @permissions_required('group_delete')
    @api.response(200, "Success")
    @api.response(404, "Could not find group")
    def delete(self, id):
        group = models.Group.query.filter(models.Group.id == id).one_or_none()

        if group is None:
            abort(404)

        db.session.delete(group)
        db.session.commit()


@api.route('/groups/<id>/users', endpoint='groupusers')
class GroupUsersAPI(Resource):
    @http_auth_required
    @permissions_accepted('group_read', 'group_read_all')
    @api.marshal_with(user_list_get)
    @api.response(200, "Success")
    @api.response(403, "You are not authorized to get this information")
    @api.response(404, "Could not find group")
    def get(self, id):
        group = models.Group.query.filter(models.Group.id == id).one_or_none()

        if group is None:
            abort(404)

        if not has_permission_any('group_read_all'):
            if group not in current_user.groups:
                abort(403)

        return group
