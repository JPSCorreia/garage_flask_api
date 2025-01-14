import logging
from utils.database import db
from models.work import Work
from datetime import datetime

logger = logging.getLogger(__name__)

def get_all_works():
    """
    Retrieve all works from the database.
    :return: A list of dictionaries containing work details.
    """
    try:
        works = Work.query.all()
        return [
            {
                "work_id": work.work_id,
                "cost": work.cost,
                "created_at": work.created_at,
                "description": work.description,
                "end_date": work.end_date,
                "start_date": work.start_date,
                "status": work.status,
                "vehicle_id": work.vehicle_id,
            }
            for work in works
        ]
    except Exception as e:
        logger.error(f"Error fetching all works: {e}")
        return {"error": "Internal Server Error"}

def get_work(work_id):
    """
    Retrieve a specific work by ID.
    :param work_id: The ID of the work to retrieve.
    :return: A dictionary with work details or None if not found.
    """
    try:
        work = Work.query.get(work_id)
        if not work:
            return None
        return {
            "work_id": work.work_id,
            "cost": work.cost,
            "created_at": work.created_at,
            "description": work.description,
            "end_date": work.end_date,
            "start_date": work.start_date,
            "status": work.status,
            "vehicle_id": work.vehicle_id,
        }
    except Exception as e:
        logger.error(f"Error fetching work {work_id}: {e}")
        return {"error": "Internal Server Error"}

def create_work(cost, description, end_date, start_date, status, vehicle_id):
    """
    Create a new work entry in the database.
    :param cost: The cost of the work.
    :param description: Description of the work.
    :param end_date: End date of the work.
    :param start_date: Start date of the work.
    :param status: Status of the work.
    :param vehicle_id: ID of the vehicle associated with the work.
    :return: A dictionary with the created work details.
    """
    try:
        work = Work(
            cost=cost,
            description=description,
            end_date=datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else None,
            start_date=datetime.strptime(start_date, "%Y-%m-%d").date(),
            status=status,
            vehicle_id=vehicle_id
        )
        db.session.add(work)
        db.session.commit()
        return {
            "work_id": work.work_id,
            "cost": work.cost,
            "created_at": work.created_at,
            "description": work.description,
            "end_date": work.end_date,
            "start_date": work.start_date,
            "status": work.status,
            "vehicle_id": work.vehicle_id,
        }
    except Exception as e:
        logger.error(f"Error creating work: {e}")
        return {"error": "Internal Server Error"}

def update_work(work_id, cost=None, description=None, end_date=None, start_date=None, status=None, vehicle_id=None):
    """
    Update an existing work entry in the database.
    :param work_id: The ID of the work to update.
    :param cost: The updated cost of the work.
    :param description: Updated description of the work.
    :param end_date: Updated end date of the work.
    :param start_date: Updated start date of the work.
    :param status: Updated status of the work.
    :param vehicle_id: Updated vehicle ID associated with the work.
    :return: A dictionary with the updated work details or None if not found.
    """
    try:
        work = Work.query.get(work_id)
        if not work:
            return None

        work.cost = cost if cost else work.cost
        work.description = description if description else work.description
        work.end_date = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else work.end_date
        work.start_date = datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else work.start_date
        work.status = status if status else work.status
        work.vehicle_id = vehicle_id if vehicle_id else work.vehicle_id

        db.session.commit()
        return {
            "work_id": work.work_id,
            "cost": work.cost,
            "created_at": work.created_at,
            "description": work.description,
            "end_date": work.end_date,
            "start_date": work.start_date,
            "status": work.status,
            "vehicle_id": work.vehicle_id,
        }
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating work {work_id}: {e}")
        return {"error": "Internal Server Error"}

def delete_work(work_id):
    """
    Delete a work entry from the database.
    :param work_id: The ID of the work to delete.
    :return: The deleted work details or None if not found.
    """
    try:
        work = Work.query.get(work_id)
        if not work:
            return None

        db.session.delete(work)
        db.session.commit()
        return {
            "work_id": work.work_id,
            "cost": work.cost,
            "description": work.description,
        }
    except Exception as e:
        logger.error(f"Error deleting work {work_id}: {e}")
        return {"error": "Internal Server Error"}
