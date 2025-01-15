import logging
from flask_restx import Namespace, Resource
from werkzeug.exceptions import HTTPException
from services.setting_service import (
    get_all_settings,
    get_setting,
    create_setting,
    update_setting,
    delete_setting
)
from utils.utils import generate_swagger_model
from models.setting import Setting

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Namespace for managing settings
setting_ns = Namespace('setting', description='CRUD operations for managing settings')

# Generate the Swagger model for the setting resource
setting_model = generate_swagger_model(
    api=setting_ns,
    model=Setting,
    exclude_fields=[],
    readonly_fields=['setting_id', 'updated_at']
)

@setting_ns.route('/')
class SettingList(Resource):
    @setting_ns.marshal_list_with(setting_model)
    def get(self):
        return get_all_settings()

    @setting_ns.expect(setting_model, validate=True)
    @setting_ns.marshal_with(setting_model, code=201)
    def post(self):
        data = setting_ns.payload
        return create_setting(data["key_name"], data["value"]), 201

@setting_ns.route('/<int:setting_id>')
class Setting(Resource):
    @setting_ns.marshal_with(setting_model)
    def get(self, setting_id):
        return get_setting(setting_id)

    @setting_ns.expect(setting_model, validate=True)
    @setting_ns.marshal_with(setting_model)
    def put(self, setting_id):
        data = setting_ns.payload
        return update_setting(setting_id, data.get("key_name"), data.get("value"))

    def delete(self, setting_id):
        return delete_setting(setting_id), 204
