from flask import Blueprint
from flask_restx import Api

# Main Blueprint for all API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Flask-RESTx Api instance
api = Api(
    api_bp,
    version='1.0',  # API version
    title='Garage API',  # Title displayed in the Swagger documentation
    description='API Swagger documentation',  # Description displayed in the Swagger documentation
    doc='/docs'  # Documentation URL (http://127.0.0.1:5000/api/docs)
)

# Import namespaces in the desired order
from .workflow import workflow_ns
from .client import clients_ns
from .employee import employees_ns
from .vehicle import vehicles_ns
from .work import works_ns
from .task import tasks_ns
from .invoice import invoice_ns
from .invoice_item import invoice_items_ns
from .setting import setting_ns

# Add namespaces in the desired order
api.add_namespace(workflow_ns, path='/workflow')  # Workflow operations first
api.add_namespace(clients_ns, path='/client')  # Client operations
api.add_namespace(employees_ns, path='/employee')  # Employee operations
api.add_namespace(vehicles_ns, path='/vehicle')  # Vehicle operations
api.add_namespace(works_ns, path='/work')  # Work operations
api.add_namespace(tasks_ns, path='/task')  # Task operations
api.add_namespace(invoice_ns, path='/invoice')  # Invoice operations
api.add_namespace(invoice_items_ns, path='/invoice_item')  # Invoice item operations
api.add_namespace(setting_ns, path='/setting')  # Setting operations
