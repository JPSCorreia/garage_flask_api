from services.client_service import create_client
from services.vehicle_service import create_vehicle
from services.work_service import create_work
from services.task_service import create_task
from services.invoice_service import create_invoice
from services.invoice_item_service import create_invoice_item
from sqlalchemy.exc import IntegrityError
from utils.database import db
from models.vehicle import Vehicle
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def register_client_and_vehicle(client_data, vehicle_data):
    """
    Register a new client and their corresponding vehicle in a single transaction.
    """
    try:
        with db.session.begin():  # Iniciar a transação
            # Criar o cliente sem fazer commit
            client = create_client(
                client_data["name"],
                client_data["email"],
                client_data["phone"],
                client_data["address"],
                commit=False  # Não faz commit aqui
            )

            # Verificar se já existe um veículo com a mesma matrícula
            existing_vehicle = Vehicle.query.filter_by(license_plate=vehicle_data["license_plate"]).first()
            if existing_vehicle:
                raise ValueError(f"Vehicle with license plate {vehicle_data['license_plate']} already exists.")

            # Criar o veículo associado ao cliente sem fazer commit
            vehicle = create_vehicle(
                vehicle_data["brand"],
                client["client_id"],
                vehicle_data["license_plate"],
                vehicle_data["model"],
                vehicle_data["year"],
                commit=False  # Não faz commit aqui
            )

            # Serializar campos datetime antes de retornar
            client["created_at"] = client["created_at"].strftime("%Y-%m-%d %H:%M:%S")
            vehicle["created_at"] = vehicle["created_at"].strftime("%Y-%m-%d %H:%M:%S")

            # Retornar os dados do cliente e veículo
            return {
                "client": client,
                "vehicle": vehicle
            }
    except ValueError as e:
        # Reverter a transação se ocorrer um erro de validação
        db.session.rollback()
        return {"error": str(e)}
    except Exception as e:
        # Reverter a transação em caso de erro inesperado
        db.session.rollback()
        logger.error(f"Error registering client and vehicle: {e}")
        return {"error": "Internal Server Error"}

#TODO: review
def create_work_for_vehicle(vehicle_id, work_data):
    """
    Create a new work associated with a vehicle.
    """
    try:
        work = create_work(
            work_data["cost"],
            work_data["start_date"],
            work_data.get("end_date"),
            work_data["status"],
            vehicle_id
        )
        if "error" in work:
            return {"error": "Failed to create work"}
        return work
    except Exception as e:
        logger.error(f"Error creating work for vehicle {vehicle_id}: {e}")
        return {"error": "Internal Server Error"}

#TODO: review
def add_tasks_to_work(work_id, tasks):
    """
    Add multiple tasks to a work.
    """
    try:
        created_tasks = []
        for task_data in tasks:
            task = create_task(
                work_id,
                task_data["employee_id"],
                task_data["description"],
                task_data["start_date"],
                task_data.get("end_date"),
                task_data["status"]
            )
            if "error" in task:
                return {"error": f"Failed to create task: {task_data['description']}"}
            created_tasks.append(task)
        return created_tasks
    except Exception as e:
        logger.error(f"Error adding tasks to work {work_id}: {e}")
        return {"error": "Internal Server Error"}

def generate_invoice_for_work(work_id):
    """
    Generate an invoice for a given work ID using the CRUD services.
    """
    try:
        # Obter todas as tarefas concluídas associadas ao trabalho
        tasks = Task.query.filter_by(work_id=work_id, status="completed").all()
        if not tasks:
            return {"error": "No completed tasks found for the given work ID"}

        # Obter o cliente associado ao trabalho
        work = Work.query.get(work_id)
        vehicle = Vehicle.query.get(work.vehicle_id)
        client_id = vehicle.client_id

        # Criar a fatura
        total = sum(task.cost for task in tasks)
        iva = total * 0.23
        total_with_iva = total + iva
        invoice = create_invoice(client_id, datetime.now(), total, iva, total_with_iva)

        # Criar itens da fatura para cada tarefa
        for task in tasks:
            create_invoice_item(task.description, task.cost, task.task_id, invoice["invoice_id"])

        return invoice
    except Exception as e:
        logger.error(f"Error generating invoice for work {work_id}: {e}")
        return {"error": "Internal Server Error"}