import pkg_resources

from flask import url_for
from flask import current_app
from flask import Blueprint
from flask_restplus import Api
from flask_restplus import Resource
from flask_restplus import fields
from sqlalchemy.exc import SQLAlchemyError

from . import RegisteredApi

blueprint = Blueprint('health_api', __name__)


api = Api(
    blueprint,
    version='1.0',
    title='Taskmanager health REST API',
    description='The TaskManager is for tracking experiments and study resources.',
    default_mediatype='application/json'
)


@api.route('/healthy', endpoint='healthy')
class Healthy(Resource):
    @api.doc('Endpoint to check if flask app is running')
    @api.response(200, 'Healthy')
    def get(self):
        return


@api.route('/ready', endpoint='ready')
class Ready(Resource):
    @api.doc('Endpoint to check if flask app ready (e.g. all resources are available and functioning)')
    @api.response(200, 'Ready')
    @api.response(500, 'Not ready')
    def get(self):
        try:
            from taskmanager import models
            # Get the task template, without templates the taskmanager is basically useless.
            models.TaskTemplate.query.first()
            return None
        except SQLAlchemyError:
            return None, 500


versions_model = {
    'version': fields.String,
    'api_versions': fields.Raw,
}


@api.route('/versions', endpoint='versions')
class Versions(Resource):
    @api.doc('Versions of the APIs available')
    @api.response(200, 'Success')
    @api.marshal_with(versions_model)
    def get(self):
        versions = {k: url_for(f"{v.name}.root") for k, v in RegisteredApi.api_map.items()}
        return {
            'version': pkg_resources.require('task-manager')[0].version,
            'api_versions': versions

        }
