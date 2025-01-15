from utils.database import db

class Task(db.Model):
    """
    Represents a task in the database.

    Attributes:
        task_id (int): Primary key for the task table.
        description (str): Description of the task.
        employee_id (int): Foreign key linking the task to an employee.
        work_id (int): Foreign key linking the task to a work.
        start_date (date): Start date of the task.
        end_date (date): End date of the task.
        status (str): Status of the task (e.g., pending, in progress, completed).
        created_at (datetime): Timestamp when the task record was created.
    """
    __tablename__ = 'task'

    task_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=False)
    work_id = db.Column(db.Integer, db.ForeignKey('work.work_id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<Task {self.description}>"
