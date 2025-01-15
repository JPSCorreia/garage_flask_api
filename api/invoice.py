import logging
from flask_restx import Namespace, Resource
from werkzeug.exceptions import HTTPException
from services.invoice_service import (
    get_all_invoices,
    get_invoice,
    create_invoice,
    update_invoice,
    delete_invoice
)
from utils.utils import generate_swagger_model
from models.invoice import Invoice

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Namespace for managing invoices
invoice_ns = Namespace('invoice', description='CRUD operations for managing invoices')

# Generate the Swagger model for the invoice resource
invoice_model = generate_swagger_model(
    api=invoice_ns,
    model=Invoice,
    exclude_fields=[],
    readonly_fields=['invoice_id', 'total_with_iva']
)

@invoice_ns.route('/')
class InvoiceList(Resource):
    @invoice_ns.marshal_list_with(invoice_model)
    def get(self):
        return get_all_invoices()

    @invoice_ns.expect(invoice_model, validate=True)
    @invoice_ns.marshal_with(invoice_model, code=201)
    def post(self):
        data = invoice_ns.payload
        return create_invoice(
            data["client_id"], data["issued_at"], data["total"], data["iva"]
        ), 201

@invoice_ns.route('/<int:invoice_id>')
class Invoice(Resource):
    @invoice_ns.marshal_with(invoice_model)
    def get(self, invoice_id):
        return get_invoice(invoice_id)

    @invoice_ns.expect(invoice_model, validate=True)
    @invoice_ns.marshal_with(invoice_model)
    def put(self, invoice_id):
        data = invoice_ns.payload
        return update_invoice(
            invoice_id, data.get("client_id"), data.get("issued_at"),
            data.get("total"), data.get("iva")
        )

    def delete(self, invoice_id):
        return delete_invoice(invoice_id), 204
