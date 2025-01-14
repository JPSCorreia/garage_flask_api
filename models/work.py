from utils.database import db

class Work(db.Model):
    """
    Represents a work (repair/job) associated with a vehicle.

    Attributes:
        work_id (int): Primary key for the work table.
        cost (float): The cost of the repair/job.
        created_at (datetime): Timestamp when the work was created.
        description (str): Description of the work.
        end_date (date): End date of the work.
        start_date (date): Start date of the work.
        status (str): The status of the work (e.g., pending, in progress, completed).
        vehicle_id (int): Foreign key linking the work to a vehicle.
    """
    __tablename__ = 'work'

    work_id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    description = db.Column(db.Text, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.vehicle_id'), nullable=False)

    def __repr__(self):
        return f"<Work {self.description}>"
