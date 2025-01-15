import logging
from flask_restx import Namespace, Resource
from werkzeug.exceptions import HTTPException
from services.invoice_item_service import (
    get_all_invoice_items,
    get_invoice_item,
    create_invoice_item,
    update_invoice_item,
    delete_invoice_item
)
from utils.utils import generate_swagger_model
from models.invoice_item import InvoiceItem

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Namespace for managing invoice items
invoice_items_ns = Namespace('invoice_item', description='CRUD operations for managing invoice items')

# Generate the Swagger model for the invoice item resource
invoice_item_model = generate_swagger_model(
    api=invoice_items_ns,
    model=InvoiceItem,
    exclude_fields=[],
    readonly_fields=['item_id']
)

@invoice_items_ns.route('/')
class InvoiceItemList(Resource):
    @invoice_items_ns.marshal_list_with(invoice_item_model)
    def get(self):
        return get_all_invoice_items()

    @invoice_items_ns.expect(invoice_item_model, validate=True)
    @invoice_items_ns.marshal_with(invoice_item_model, code=201)
    def post(self):
        data = invoice_items_ns.payload
        return create_invoice_item(
            data["description"], data["cost"], data["task_id"], data["invoice_id"]
        ), 201

@invoice_items_ns.route('/<int:item_id>')
class InvoiceItem(Resource):
    @invoice_items_ns.marshal_with(invoice_item_model)
    def get(self, item_id):
        return get_invoice_item(item_id)

    @invoice_items_ns.expect(invoice_item_model, validate=True)
    @invoice_items_ns.marshal_with(invoice_item_model)
    def put(self, item_id):
        data = invoice_items_ns.payload
        return update_invoice_item(
            item_id, data.get("description"), data.get("cost"),
            data.get("task_id"), data.get("invoice_id")
        )

    def delete(self, item_id):
        return delete_invoice_item(item_id), 204