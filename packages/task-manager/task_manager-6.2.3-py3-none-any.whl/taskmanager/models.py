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

import datetime
import threading

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_security import SQLAlchemyUserDatastore

from sqlalchemy.sql import func
from sqlalchemy.orm.exc import NoResultFound

from .callbacks import dispatch_callback
from .auth.models import BaseUser
from .auth.models import BaseRole

db = SQLAlchemy()

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id', name="fk_roles_users_user_id_user")),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id', name="fk_roles_users_role_id_role")))


class Role(db.Model, BaseRole):
    """ This implements the BaseRole from the .auth.models module.
    In this specific case, the BaseRole is sufficient. """
    __tablename__ = 'role'
    pass


class TaskGroupLinks(db.Model):
    __tablename__ = 'task_group_links'

    task_id = db.Column(db.Integer, db.ForeignKey('task.id', name="fk_task_group_links_task_id_task"), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id', name="fk_task_group_links_group_id_group"), primary_key=True)


class TaskUserLinks(db.Model):
    __tablename__ = 'task_user_links'

    task_id = db.Column(db.Integer, db.ForeignKey('task.id', name="fk_task_user_links_task_id_task"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name="fk_task_user_links_user_id_user"), primary_key=True)
    create_time = db.Column(db.DateTime(timezone=True), default=func.now())


class TagTaskLinks(db.Model):
    __tablename__ = 'tag_task_links'

    task_id = db.Column(db.Integer, db.ForeignKey('task.id', name="fk_tag_task_links_task_id_task"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id', name="fk_tag_task_links_tag_id_tag"), primary_key=True)


class TaskTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.VARCHAR(64), unique=True, nullable=False)
    content = db.Column(db.Text)
    tasks = db.relationship("Task", back_populates="template")

    def __init__(self, label, content):
        self.label = label
        self.content = content


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.VARCHAR(64))
    _status = db.Column("status", db.VARCHAR(32))
    lock_id = db.Column(db.Integer, db.ForeignKey('user.id', name="fk_task_lock_id_user"))
    lock = db.relationship("User", uselist=False)
    content = db.Column(db.Text)
    callback_url = db.Column(db.Text)
    callback_content = db.Column(db.Text)
    tags = db.relationship("Tag", secondary="tag_task_links", backref=db.backref("tasks"))
    parent_id = db.Column(db.Integer, db.ForeignKey('task_group.id', name='fk_task_parent_id_task_group'))
    parent = db.relationship("TaskGroup", back_populates="tasks")
    template_id = db.Column(db.Integer, db.ForeignKey('task_template.id', name='fk_task_template_id_task_template'))
    template = db.relationship("TaskTemplate", back_populates="tasks")
    create_time = db.Column(db.DateTime(timezone=True), default=func.now())
    update_time = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.current_timestamp())
    generator_url = db.Column(db.String(length=512), nullable=True)
    application_name = db.Column(db.VARCHAR(length=32), nullable=True)
    application_version = db.Column(db.VARCHAR(length=16), nullable=True)

    def __init__(self,
                 project,
                 template,
                 content,
                 callback_url=None,
                 callback_content=None,
                 generator_url=None,
                 application_name=None,
                 application_version=None):
        self.project = project
        self.template = template
        self.content = content
        self.status = 'queued'

        if callback_url is not None:
            self.callback_url = callback_url

        if callback_content is not None:
            self.callback_content = callback_content

        self.generator_url = generator_url
        self.application_name = application_name
        self.application_version = application_version

    def __repr__(self):
        return f'<Task {self.id}, project: {self.project}, template: {self.template.label}>'

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

        # If the task is set to done, automatically call the callback in a background thread
        if value == 'done':
            if self.callback_url is not None:
                callback_thead = threading.Thread(target=dispatch_callback,
                                                  name=f"callback_thread_{self.id}",
                                                  kwargs={'url': self.callback_url,
                                                          'content': self.callback_content,
                                                          'config': current_app.config})
                callback_thead.start()
            else:
                print('Task is done but no callback is set!')

        # Signal parent that a child was updated
        if self.parent is not None:
            self.parent.child_updated()


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(32), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Tag {self.name}>'


class TaskGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.VARCHAR(64), unique=True)
    callback_url = db.Column(db.Text)
    callback_content = db.Column(db.Text)
    callback_fired = db.Column(db.Boolean)
    tasks = db.relationship('Task', back_populates='parent')

    def __init__(self, label, callback_url, callback_content, tasks=None):
        self.label = label
        self.callback_url = callback_url
        self.callback_content = callback_content
        self.callback_fired = False
        if tasks is not None:
            self.tasks = tasks

    def __repr__(self):
        return f'<TaskGroup {self.label}>'

    @property
    def status(self):
        return 'done' if all(t.status == 'done' for t in self.tasks) else 'queued'

    def child_updated(self):
        if all(x.status == 'done' for x in self.tasks):
            if self.callback_url is not None and not self.callback_fired:
                self.callback_fired = True
                callback_thead = threading.Thread(target=dispatch_callback,
                                                  name=f"callback_thread_{self.id}",
                                                  kwargs={'url': self.callback_url,
                                                          'content': self.callback_content,
                                                          'config': current_app.config})
                callback_thead.start()
            else:
                print(f'TaskGroup {self.label} is done but no callback is set!')


class User(db.Model, BaseUser):
    __tablename__ = 'user'
    create_time = db.Column(db.DateTime(timezone=True), default=func.now())
    assignment_weight = db.Column(db.FLOAT, nullable=False, default=1.0)
    user_tasks = db.relationship("Task", secondary="task_user_links", backref=db.backref("users"))
    group_tasks = db.relationship("Task",
                                  secondary="join(task_group_links, group).join(group_membership)",
                                  backref=db.backref("users_via_group"))
    roles = db.relationship('Role', secondary='roles_users',
                            backref=db.backref('users', lazy='dynamic'))

    #def __init__(self, username, password, name, email, active=True, roles="user", assignment_weight=None):
    #    current_app.logger.info(f"{roles}")
    #    #BaseUser.__init__(self, username, password, name, email, roles)
    #    
    #    if self.assignment_weight is None:
    #        self.assignment_weight = assignment_weight

    def __repr__(self):
        return f'<User {self.username} ({self.name})>'

    @property
    def tasks(self):
        tasks = []
        for task in self.user_tasks:
            if task not in tasks:
                tasks.append(task)
        for task in self.group_tasks:
            if task not in tasks:
                tasks.append(task)
        return tasks

    @property
    def last_assignment(self):
        last_task = TaskUserLinks.query.filter(
            TaskUserLinks.user_id == self.id
        ).order_by(TaskUserLinks.create_time.desc()).first()

        if last_task is None:
            return datetime.datetime.min
        else:
            return last_task.create_time


class GroupMembership(db.Model):
    __tablename__ = 'group_membership'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name="fk_group_membership_user_id_user"), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id', name="fk_group_membership_group_id_group"), primary_key=True)


class Group(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    groupname = db.Column(db.VARCHAR(64), unique=True, nullable=False)
    name = db.Column(db.VARCHAR(64), unique=True, nullable=False)
    users = db.relationship("User", secondary="group_membership", backref=db.backref("groups"))
    tasks = db.relationship("Task", secondary="task_group_links", backref=db.backref("groups"))
    create_time = db.Column(db.DateTime(timezone=True), default=func.now())

    def __init__(self, groupname, name=None, members=None):
        self.groupname = groupname
        self.name = name

        if members is not None:
            for member in members:
                try:
                    user = User.query.filter(User.username == member).one()
                except NoResultFound:
                    raise NoResultFound(f"User [{member}] is not found in the taskmanager")

                self.users.append(user)

    def __repr__(self):
        return f'<Group {self.groupname} ({self.name})>'
