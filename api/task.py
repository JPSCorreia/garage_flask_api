import logging
from flask_restx import Namespace, Resource
from werkzeug.exceptions import HTTPException
from services.task_service import (
    get_all_tasks,
    get_task,
    create_task,
    update_task,
    delete_task
)
from utils.utils import generate_swagger_model
from models.task import Task

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Namespace for managing tasks
tasks_ns = Namespace('task', description='CRUD operations for managing tasks')

# Generate the Swagger model for the task resource
task_model = generate_swagger_model(
    api=tasks_ns,
    model=Task,
    exclude_fields=[],
    readonly_fields=['task_id', 'created_at']
)

@tasks_ns.route('/')
class TaskList(Resource):
    @tasks_ns.marshal_list_with(task_model)
    def get(self):
        return get_all_tasks()

    @tasks_ns.expect(task_model, validate=True)
    @tasks_ns.marshal_with(task_model, code=201)
    def post(self):
        data = tasks_ns.payload
        return create_task(
            data["description"], data["employee_id"], data["work_id"],
            data["start_date"], data.get("end_date"), data["status"]
        ), 201

@tasks_ns.route('/<int:task_id>')
class Task(Resource):
    @tasks_ns.marshal_with(task_model)
    def get(self, task_id):
        return get_task(task_id)

    @tasks_ns.expect(task_model, validate=True)
    @tasks_ns.marshal_with(task_model)
    def put(self, task_id):
        data = tasks_ns.payload
        return update_task(
            task_id, data.get("description"), data.get("employee_id"),
            data.get("work_id"), data.get("start_date"),
            data.get("end_date"), data.get("status")
        )

    def delete(self, task_id):
        return delete_task(task_id), 204
