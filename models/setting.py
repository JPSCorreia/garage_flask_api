from utils.database import db

class Setting(db.Model):
    """
    Represents a setting in the database.

    Attributes:
        setting_id (int): Primary key for the setting table.
        key_name (str): The name of the setting.
        value (str): The value of the setting.
        updated_at (datetime): Timestamp when the setting was last updated.
    """
    __tablename__ = 'setting'

    setting_id = db.Column(db.Integer, primary_key=True)
    key_name = db.Column(db.String(100), nullable=False, unique=True)
    value = db.Column(db.Text, nullable=False)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f"<Setting {self.key_name}>"
