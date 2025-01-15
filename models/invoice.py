from utils.database import db

class Invoice(db.Model):
    """
    Represents an invoice in the database.

    Attributes:
        invoice_id (int): Primary key for the invoice table.
        client_id (int): Foreign key linking the invoice to a client.
        issued_at (datetime): Date the invoice was issued.
        total (float): Total amount before VAT (IVA).
        iva (float): Value-added tax applied to the total.
        total_with_iva (float): Total amount including VAT (IVA).
        created_at (datetime): Timestamp when the invoice record was created.
    """
    __tablename__ = 'invoice'

    invoice_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), nullable=False)
    issued_at = db.Column(db.DateTime, nullable=False)
    total = db.Column(db.Float, nullable=False)
    iva = db.Column(db.Float, nullable=False)
    total_with_iva = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Invoice {self.invoice_id} for Client {self.client_id}>"
