from datetime import datetime
from utils.database import db
from models.task import Task
import logging

logger = logging.getLogger(__name__)

def get_all_tasks():
    try:
        tasks = Task.query.all()
        return [
            {
                "task_id": task.task_id,
                "description": task.description,
                "employee_id": task.employee_id,
                "work_id": task.work_id,
                "start_date": task.start_date,
                "end_date": task.end_date,
                "status": task.status,
                "created_at": task.created_at,
            }
            for task in tasks
        ]
    except Exception as e:
        logger.error(f"Error fetching all tasks: {e}")
        return {"error": "Internal Server Error"}

def get_task(task_id):
    try:
        task = Task.query.get(task_id)
        if not task:
            return None
        return {
            "task_id": task.task_id,
            "description": task.description,
            "employee_id": task.employee_id,
            "work_id": task.work_id,
            "start_date": task.start_date,
            "end_date": task.end_date,
            "status": task.status,
            "created_at": task.created_at,
        }
    except Exception as e:
        logger.error(f"Error fetching task {task_id}: {e}")
        return {"error": "Internal Server Error"}

def create_task(description, employee_id, work_id, start_date, end_date, status):
    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else None

        task = Task(
            description=description,
            employee_id=employee_id,
            work_id=work_id,
            start_date=start_date_obj,
            end_date=end_date_obj,
            status=status
        )
        db.session.add(task)
        db.session.commit()
        return {
            "task_id": task.task_id,
            "description": task.description,
            "employee_id": task.employee_id,
            "work_id": task.work_id,
            "start_date": task.start_date,
            "end_date": task.end_date,
            "status": task.status,
            "created_at": task.created_at,
        }
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        return {"error": "Internal Server Error"}

def update_task(task_id, description=None, employee_id=None, work_id=None, start_date=None, end_date=None, status=None):
    try:
        task = Task.query.get(task_id)
        if not task:
            return None

        task.description = description if description else task.description
        task.employee_id = employee_id if employee_id else task.employee_id
        task.work_id = work_id if work_id else task.work_id
        task.start_date = datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else task.start_date
        task.end_date = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else task.end_date
        task.status = status if status else task.status

        db.session.commit()
        return {
            "task_id": task.task_id,
            "description": task.description,
            "employee_id": task.employee_id,
            "work_id": task.work_id,
            "start_date": task.start_date,
            "end_date": task.end_date,
            "status": task.status,
            "created_at": task.created_at,
        }
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating task {task_id}: {e}")
        return {"error": "Internal Server Error"}

def delete_task(task_id):
    try:
        task = Task.query.get(task_id)
        if not task:
            return None

        db.session.delete(task)
        db.session.commit()
        return {"message": f"Task {task_id} deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting task {task_id}: {e}")
        return {"error": "Internal Server Error"}

def update_task_status(task_id, new_status):
    """
    Update the status of a specific task.
    :param task_id: ID of the task to update
    :param new_status: New status to be set
    :return: Dictionary with success message or error
    """
    try:
        task = Task.query.get(task_id)
        if not task:
            return {"error": f"Task with ID {task_id} not found"}

        task.status = new_status
        db.session.commit()
        return {"message": f"Task {task_id} status updated successfully to {new_status}"}

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating task {task_id} status: {e}")
        return {"error": "Internal Server Error"}