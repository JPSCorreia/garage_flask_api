import logging
from flask_restx import Namespace, Resource, fields
from services.workflow_service import register_client_and_vehicle
from services.workflow_service import create_work_for_vehicle
from services.workflow_service import add_tasks_to_work

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Namespace para workflows
workflow_ns = Namespace('workflow', description='Workflow operations for advanced functionalities')

# Modelo para Cliente
client_model = workflow_ns.model('Client', {
    'name': fields.String(required=True, description='Name of the client'),
    'email': fields.String(required=True, description='Email of the client'),
    'phone': fields.String(required=True, description='Phone number of the client'),
    'address': fields.String(required=True, description='Address of the client')
})

# Modelo para Veículo
vehicle_model = workflow_ns.model('Vehicle', {
    'brand': fields.String(required=True, description='Brand of the vehicle'),
    'model': fields.String(required=True, description='Model of the vehicle'),
    'year': fields.Integer(required=True, description='Year of the vehicle'),
    'license_plate': fields.String(required=True, description='License plate of the vehicle')
})

# Modelo para criar um trabalho (Work)
work_model = workflow_ns.model('Work', {
    'description': fields.String(required=True, description='Description of the work'),
    'cost': fields.Float(required=True, description='Cost of the work'),
    'start_date': fields.String(required=True, description='Start date (YYYY-MM-DD)'),
    'end_date': fields.String(required=False, description='End date (YYYY-MM-DD)'),
    'status': fields.String(required=True, description='Status of the work'),
    'vehicle_id': fields.Integer(required=True, description='ID of the associated vehicle')
})

# Modelo para o payload completo
register_client_and_vehicle_model = workflow_ns.model('RegisterClientVehicle', {
    'client': fields.Nested(client_model, required=True, description='Client information'),
    'vehicle': fields.Nested(vehicle_model, required=True, description='Vehicle information')
})

@workflow_ns.route('/register_client_and_vehicle')
class RegisterClientAndVehicle(Resource):
    @workflow_ns.expect(register_client_and_vehicle_model, validate=True)
    def post(self):
        """
        Register a new client and their corresponding vehicle.
        """
        data = workflow_ns.payload
        client_data = data.get("client")
        vehicle_data = data.get("vehicle")
        result = register_client_and_vehicle(client_data, vehicle_data)
        if "error" in result:
            return result, 400
        return result, 201

@workflow_ns.route('/create_work')
class CreateWork(Resource):
    @workflow_ns.expect(work_model, validate=True)  # Define o modelo esperado
    def post(self):
        """
        Create a new work associated with a vehicle.
        """
        # Obter os dados enviados no JSON
        data = workflow_ns.payload

        # Chamar a função para criar o trabalho associado ao veículo
        result = create_work_for_vehicle(data)
        if "error" in result:
            return result, 400
        return result, 201

@workflow_ns.route('/add_tasks/<int:work_id>')
class AddTasksToWork(Resource):
    def post(self, work_id):
        """
        Add multiple tasks to a work.
        """
        data = workflow_ns.payload
        result = add_tasks_to_work(work_id, data["tasks"])
        if "error" in result:
            return result, 400
        return result, 201