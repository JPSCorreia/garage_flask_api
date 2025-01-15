from utils.database import db
from models.setting import Setting
import logging

logger = logging.getLogger(__name__)

def get_all_settings():
    try:
        settings = Setting.query.all()
        return [
            {
                "setting_id": setting.setting_id,
                "key_name": setting.key_name,
                "value": setting.value,
                "updated_at": setting.updated_at,
            }
            for setting in settings
        ]
    except Exception as e:
        logger.error(f"Error fetching all settings: {e}")
        return {"error": "Internal Server Error"}

def get_setting(setting_id):
    try:
        setting = Setting.query.get(setting_id)
        if not setting:
            return None
        return {
            "setting_id": setting.setting_id,
            "key_name": setting.key_name,
            "value": setting.value,
            "updated_at": setting.updated_at,
        }
    except Exception as e:
        logger.error(f"Error fetching setting {setting_id}: {e}")
        return {"error": "Internal Server Error"}

def create_setting(key_name, value):
    try:
        setting = Setting(
            key_name=key_name,
            value=value
        )
        db.session.add(setting)
        db.session.commit()
        return {
            "setting_id": setting.setting_id,
            "key_name": setting.key_name,
            "value": setting.value,
            "updated_at": setting.updated_at,
        }
    except Exception as e:
        logger.error(f"Error creating setting: {e}")
        return {"error": "Internal Server Error"}

def update_setting(setting_id, key_name=None, value=None):
    try:
        setting = Setting.query.get(setting_id)
        if not setting:
            return None

        setting.key_name = key_name if key_name else setting.key_name
        setting.value = value if value else setting.value

        db.session.commit()
        return {
            "setting_id": setting.setting_id,
            "key_name": setting.key_name,
            "value": setting.value,
            "updated_at": setting.updated_at,
        }
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating setting {setting_id}: {e}")
        return {"error": "Internal Server Error"}

def delete_setting(setting_id):
    try:
        setting = Setting.query.get(setting_id)
        if not setting:
            return None

        db.session.delete(setting)
        db.session.commit()
        return {"message": f"Setting {setting_id} deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting setting {setting_id}: {e}")
        return {"error": "Internal Server Error"}
