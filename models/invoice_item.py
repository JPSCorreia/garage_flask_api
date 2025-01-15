from utils.database import db

class InvoiceItem(db.Model):
    """
    Represents an item in an invoice.

    Attributes:
        item_id (int): Primary key for the invoice_item table.
        description (str): Description of the item.
        cost (float): Cost of the item.
        task_id (int): Foreign key linking the item to a task.
        invoice_id (int): Foreign key linking the item to an invoice.
    """
    __tablename__ = 'invoice_item'

    item_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.task_id'), nullable=False)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.invoice_id'), nullable=False)

    def __repr__(self):
        return f"<InvoiceItem {self.description}>"