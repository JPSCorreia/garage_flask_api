import logging
from flask_restx import Namespace, Resource, fields
from werkzeug.exceptions import HTTPException
from services.work_service import (
    get_all_works,
    get_work,
    create_work,
    update_work,
    delete_work,
    update_work_status
)
from utils.utils import generate_swagger_model
from models.work import Work

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Namespace for managing works
works_ns = Namespace('work', description='CRUD operations for managing works')

# Generate the Swagger model for the work resource
work_model = generate_swagger_model(
    api=works_ns,
    model=Work,
    exclude_fields=[],
    readonly_fields=['work_id']
)

@works_ns.route('/')
class WorkList(Resource):
    @works_ns.marshal_list_with(work_model)
    def get(self):
        return get_all_works()

    @works_ns.expect(work_model, validate=True)
    @works_ns.marshal_with(work_model, code=201)
    def post(self):
        data = works_ns.payload
        return create_work(
            data["cost"], data["description"], data.get("end_date"),
            data["start_date"], data["status"], data["vehicle_id"]
        ), 201

@works_ns.route('/<int:work_id>')
class Work(Resource):
    @works_ns.marshal_with(work_model)
    def get(self, work_id):
        return get_work(work_id)

    @works_ns.expect(work_model, validate=True)
    @works_ns.marshal_with(work_model)
    def put(self, work_id):
        data = works_ns.payload
        return update_work(
            work_id, data.get("cost"), data.get("description"), data.get("end_date"),
            data.get("start_date"), data.get("status"), data.get("vehicle_id")
        )

    def delete(self, work_id):
        return delete_work(work_id), 204

@works_ns.route('/<int:work_id>/status')
class UpdateWorkStatus(Resource):
    @works_ns.expect(works_ns.model('WorkStatusUpdate', {
        'status': fields.String(required=True, description='New status of the work')
    }))
    def put(self, work_id):
        """
        Update the status of a specific work.
        """
        data = works_ns.payload
        result = update_work_status(work_id, data["status"])
        if "error" in result:
            return result, 400
        return result, 200
