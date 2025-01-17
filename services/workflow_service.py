from services.client_service import create_client
from services.vehicle_service import create_vehicle
from services.work_service import create_work
from services.task_service import create_task
from services.invoice_service import create_invoice
from services.invoice_item_service import create_invoice_item
from sqlalchemy.exc import IntegrityError
from utils.database import db
from models.vehicle import Vehicle
from models.work import Work  
from models.task import Task
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

def create_work_for_vehicle(work_data):
    """
    Create a new work associated with a vehicle.
    :param work_data: Dictionary containing work details.
    :return: Dictionary with the created work details or an error message.
    """
    try:
        # Criar o trabalho associado ao veículo
        work = create_work(
            work_data["cost"],
            work_data["description"],
            work_data["start_date"],
            work_data.get("end_date"),
            work_data["status"],
            work_data["vehicle_id"],
        )
        
        # Verificar se ocorreu algum erro durante a criação
        if "error" in work:
            return {"error": "Failed to create work"}

        # Serializar os campos datetime antes de retornar
        work["start_date"] = work["start_date"].strftime("%Y-%m-%d")
        work["end_date"] = work["end_date"].strftime("%Y-%m-%d") if work["end_date"] else None
        work["created_at"] = work["created_at"].strftime("%Y-%m-%d %H:%M:%S")

        return work
    except KeyError as e:
        # Erro de campo em falta no dicionário
        logger.error(f"Missing field in work data: {e}")
        return {"error": f"Missing field in work data: {str(e)}"}
    except Exception as e:
        # Erro geral
        logger.error(f"Error creating work: {e}")
        return {"error": "Internal Server Error"}


from datetime import datetime

def add_tasks_to_work(work_id, tasks_data):
    """
    Add multiple tasks to a specific work.
    """
    try:
        tasks_to_add = []
        for task_data in tasks_data:
            start_date = datetime.strptime(task_data["start_date"], "%Y-%m-%d").date()
            end_date = datetime.strptime(task_data["end_date"], "%Y-%m-%d").date() if task_data.get("end_date") else None
            
            task = Task(
                description=task_data["description"],
                employee_id=task_data["employee_id"],
                work_id=work_id,
                start_date=start_date,
                end_date=end_date,
                status=task_data["status"]
            )
            tasks_to_add.append(task)

        db.session.add_all(tasks_to_add)
        db.session.commit()
        return {"message": f"Successfully added {len(tasks_to_add)} tasks to work {work_id}"}
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding tasks to work {work_id}: {e}")
        return {"error": "Internal Server Error"}
