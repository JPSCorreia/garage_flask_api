from utils.database import db


# Model definition for the 'Vehicle' table
class Vehicle(db.Model):
    """
    Represents a vehicle in the database.

    Attributes:
        vehicle_id (int): The primary key for the vehicle table.
        brand (str): The brand of the vehicle. Cannot be null.
        client_id (int): The ID of the client associated with the vehicle. Cannot be null.
        created_at (datetime): Timestamp when the vehicle was created. Defaults to the current time.
        license_plate (str): The license plate of the vehicle. Cannot be null.
        model (str): The model of the vehicle. Cannot be null.
        year (int): The year of the vehicle. Cannot be null.        
    """

    # Define columns for the table
    vehicle_id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(80), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    license_plate = db.Column(db.String(20), nullable=False)
    model = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """
        String representation of the Vehicle object.
        Useful for debugging and logging purposes.
        """
        return f"<Vehicle {self.license_plate}>"