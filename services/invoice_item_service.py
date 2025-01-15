from utils.database import db
from models.invoice_item import InvoiceItem
import logging

logger = logging.getLogger(__name__)

def get_all_invoice_items():
    try:
        items = InvoiceItem.query.all()
        return [
            {
                "item_id": item.item_id,
                "description": item.description,
                "cost": item.cost,
                "task_id": item.task_id,
                "invoice_id": item.invoice_id,
            }
            for item in items
        ]
    except Exception as e:
        logger.error(f"Error fetching all invoice items: {e}")
        return {"error": "Internal Server Error"}

def get_invoice_item(item_id):
    try:
        item = InvoiceItem.query.get(item_id)
        if not item:
            return None
        return {
            "item_id": item.item_id,
            "description": item.description,
            "cost": item.cost,
            "task_id": item.task_id,
            "invoice_id": item.invoice_id,
        }
    except Exception as e:
        logger.error(f"Error fetching invoice item {item_id}: {e}")
        return {"error": "Internal Server Error"}

def create_invoice_item(description, cost, task_id, invoice_id):
    try:
        item = InvoiceItem(
            description=description,
            cost=cost,
            task_id=task_id,
            invoice_id=invoice_id
        )
        db.session.add(item)
        db.session.commit()
        return {
            "item_id": item.item_id,
            "description": item.description,
            "cost": item.cost,
            "task_id": item.task_id,
            "invoice_id": item.invoice_id,
        }
    except Exception as e:
        logger.error(f"Error creating invoice item: {e}")
        return {"error": "Internal Server Error"}

def update_invoice_item(item_id, description=None, cost=None, task_id=None, invoice_id=None):
    try:
        item = InvoiceItem.query.get(item_id)
        if not item:
            return None

        item.description = description if description else item.description
        item.cost = cost if cost else item.cost
        item.task_id = task_id if task_id else item.task_id
        item.invoice_id = invoice_id if invoice_id else item.invoice_id

        db.session.commit()
        return {
            "item_id": item.item_id,
            "description": item.description,
            "cost": item.cost,
            "task_id": item.task_id,
            "invoice_id": item.invoice_id,
        }
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating invoice item {item_id}: {e}")
        return {"error": "Internal Server Error"}

def delete_invoice_item(item_id):
    try:
        item = InvoiceItem.query.get(item_id)
        if not item:
            return None

        db.session.delete(item)
        db.session.commit()
        return {"message": f"Invoice item {item_id} deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting invoice item {item_id}: {e}")
        return {"error": "Internal Server Error"}
