from datetime import datetime
from utils.database import db
from models.invoice import Invoice
import logging

logger = logging.getLogger(__name__)

def get_all_invoices():
    try:
        invoices = Invoice.query.all()
        return [
            {
                "invoice_id": invoice.invoice_id,
                "client_id": invoice.client_id,
                "issued_at": invoice.issued_at,
                "total": invoice.total,
                "iva": invoice.iva,
                "total_with_iva": invoice.total_with_iva,
            }
            for invoice in invoices
        ]
    except Exception as e:
        logger.error(f"Error fetching all invoices: {e}")
        return {"error": "Internal Server Error"}

def get_invoice(invoice_id):
    try:
        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            return None
        return {
            "invoice_id": invoice.invoice_id,
            "client_id": invoice.client_id,
            "issued_at": invoice.issued_at,
            "total": invoice.total,
            "iva": invoice.iva,
            "total_with_iva": invoice.total_with_iva,
        }
    except Exception as e:
        logger.error(f"Error fetching invoice {invoice_id}: {e}")
        return {"error": "Internal Server Error"}

def create_invoice(client_id, issued_at, total, iva):
    try:
        issued_at_obj = datetime.strptime(issued_at, "%Y-%m-%d").date()
        total_with_iva = total + iva

        invoice = Invoice(
            client_id=client_id,
            issued_at=issued_at_obj,
            total=total,
            iva=iva,
            total_with_iva=total_with_iva
        )
        db.session.add(invoice)
        db.session.commit()
        return {
            "invoice_id": invoice.invoice_id,
            "client_id": invoice.client_id,
            "issued_at": invoice.issued_at,
            "total": invoice.total,
            "iva": invoice.iva,
            "total_with_iva": invoice.total_with_iva,
        }
    except Exception as e:
        logger.error(f"Error creating invoice: {e}")
        return {"error": "Internal Server Error"}

def update_invoice(invoice_id, client_id=None, issued_at=None, total=None, iva=None):
    try:
        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            return None

        invoice.client_id = client_id if client_id else invoice.client_id
        invoice.issued_at = datetime.strptime(issued_at, "%Y-%m-%d").date() if issued_at else invoice.issued_at
        invoice.total = total if total else invoice.total
        invoice.iva = iva if iva else invoice.iva
        invoice.total_with_iva = invoice.total + invoice.iva

        db.session.commit()
        return {
            "invoice_id": invoice.invoice_id,
            "client_id": invoice.client_id,
            "issued_at": invoice.issued_at,
            "total": invoice.total,
            "iva": invoice.iva,
            "total_with_iva": invoice.total_with_iva,
        }
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating invoice {invoice_id}: {e}")
        return {"error": "Internal Server Error"}

def delete_invoice(invoice_id):
    try:
        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            return None

        db.session.delete(invoice)
        db.session.commit()
        return {"message": f"Invoice {invoice_id} deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting invoice {invoice_id}: {e}")
        return {"error": "Internal Server Error"}
