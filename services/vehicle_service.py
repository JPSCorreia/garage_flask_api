import logging
from utils.database import db
from models.vehicle import Vehicle

logger = logging.getLogger(__name__)

def get_all_vehicles():
    """
    Retrieve all vehicles from the database.
    :return: A list of dictionaries containing vehicle information.
    """
    try:
        vehicles = Vehicle.query.all()
        return [
            {
                "vehicle_id": vehicle.vehicle_id,
                "brand": vehicle.brand,
                "client_id": vehicle.client_id,
                "created_at": vehicle.created_at,
                "license_plate": vehicle.license_plate,
                "model": vehicle.model,
                "year": vehicle.year,
            }
            for vehicle in vehicles
        ]
    except Exception as e:
        logger.error(f"Error fetching all vehicles: {e}")
        return {"error": "Internal Server Error"}

def get_vehicle(vehicle_id):
    """
    Retrieve a vehicle by ID.
    :param vehicle_id: The ID of the vehicle to retrieve.
    :return: A dictionary containing the vehicle's information or None if not found.
    """
    try:
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            return None
        return {
            "vehicle_id": vehicle.vehicle_id,
            "brand": vehicle.brand,
            "client_id": vehicle.client_id,
            "created_at": vehicle.created_at,
            "license_plate": vehicle.license_plate,
            "model": vehicle.model,
            "year": vehicle.year,
        }
    except Exception as e:
        logger.error(f"Error fetching vehicle {vehicle_id}: {e}")
        return {"error": "Internal Server Error"}

def create_vehicle(brand, client_id, license_plate, model, year, commit=True):
    """
    Create a new vehicle.
    :param brand: The brand of the vehicle.
    :param client_id: The ID of the client associated with the vehicle.
    :param license_plate: The license plate of the vehicle.
    :param model: The model of the vehicle.
    :param year: The year of the vehicle.
    :param commit: A boolean indicating whether to commit the transaction immediately.
    :return: A dictionary containing the newly created vehicle's information or an error message.
    """
    try:
        # Create a new vehicle instance
        vehicle = Vehicle(
            brand=brand,
            client_id=client_id,
            license_plate=license_plate,
            model=model,
            year=year
        )
        db.session.add(vehicle)  # Add the vehicle to the current session
        db.session.flush()  # Ensure the vehicle_id is generated

        # Commit the transaction only if `commit` is True
        if commit:
            db.session.commit()

        # Return the vehicle details
        return {
            "vehicle_id": vehicle.vehicle_id,
            "brand": vehicle.brand,
            "client_id": vehicle.client_id,
            "created_at": vehicle.created_at,
            "license_plate": vehicle.license_plate,
            "model": vehicle.model,
            "year": vehicle.year,
        }
    except Exception as e:
        # Rollback the transaction only if `commit` is True
        if commit:
            db.session.rollback()
        logger.error(f"Error creating vehicle: {e}")
        return {"error": "Internal Server Error"}


def update_vehicle(vehicle_id, brand=None, client_id=None, license_plate=None, model=None, year=None):
    """
    Update an existing vehicle.
    :param vehicle_id: The ID of the vehicle to update.
    :param brand: The new brand of the vehicle.
    :param client_id: The new client ID associated with the vehicle.
    :param license_plate: The new license plate of the vehicle.
    :param model: The new model of the vehicle.
    :param year: The new year of the vehicle.
    :return: A dictionary containing the updated vehicle's information or None if not found.
    """
    try:
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            return None

        # Update the fields if new values are provided
        vehicle.brand = brand if brand else vehicle.brand
        vehicle.client_id = client_id if client_id else vehicle.client_id
        vehicle.license_plate = license_plate if license_plate else vehicle.license_plate
        vehicle.model = model if model else vehicle.model
        vehicle.year = year if year else vehicle.year

        db.session.commit()
        return {
            "vehicle_id": vehicle.vehicle_id,
            "brand": vehicle.brand,
            "client_id": vehicle.client_id,
            "created_at": vehicle.created_at,
            "license_plate": vehicle.license_plate,
            "model": vehicle.model,
            "year": vehicle.year,
        }
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating vehicle {vehicle_id}: {e}")
        return {"error": "Internal Server Error"}

def delete_vehicle(vehicle_id):
    """
    Delete a vehicle.
    :param vehicle_id: The ID of the vehicle to delete.
    :return: The deleted vehicle's information or None if not found.
    """
    try:
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            return None

        db.session.delete(vehicle)
        db.session.commit()
        return {
            "vehicle_id": vehicle.vehicle_id,
            "brand": vehicle.brand,
            "client_id": vehicle.client_id,
            "created_at": vehicle.created_at,
            "license_plate": vehicle.license_plate,
            "model": vehicle.model,
            "year": vehicle.year,
        }
    except Exception as e:
        logger.error(f"Error deleting vehicle {vehicle_id}: {e}")
        return {"error": "Internal Server Error"}
