import csv
from datetime import datetime

@pyscript_executor
def write_sensor_csv(filename, data):
    """Write sensor CSV file."""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            if not data:
                return None, "No data to write"
            
            fieldnames = list(data[0].keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
            
        return len(data), None
    except Exception as exc:
        return None, str(exc)

@service
def export_sensors_only():
    """Export only sensor entities with key attributes."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"/config/exports/sensors_export_{timestamp}.csv"
    
    log.info(f"Exporting sensor entities to {filename}")
    
    # Get only sensor entities
    sensor_ids = state.names("sensor")
    
    sensors_data = []
    
    for sensor_id in sensor_ids:
        try:
            sensor_state = state.get(sensor_id)
            attrs = state.getattr(sensor_id) or {}
            
            # Create structured row with key sensor attributes
            row = {
                'entity_id': sensor_id,
                'state': sensor_state,
                'friendly_name': attrs.get('friendly_name', ''),
                'unit_of_measurement': attrs.get('unit_of_measurement', ''),
                'device_class': attrs.get('device_class', ''),
                'state_class': attrs.get('state_class', ''),
                'last_changed': attrs.get('last_changed', ''),
                'last_updated': attrs.get('last_updated', ''),
            }
            
            sensors_data.append(row)
            
        except Exception as exc:
            log.warning(f"Error processing {sensor_id}: {exc}")
    
    count, error = write_sensor_csv(filename, sensors_data)
    
    if error:
        log.error(f"Sensor export failed: {error}")
    else:
        log.info(f"Exported {count} sensors successfully")
        persistent_notification.create(
            title="Sensor Export Complete",
            message=f"Exported {count} sensors to {filename}"
        )