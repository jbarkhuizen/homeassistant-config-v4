#!/usr/bin/env python3
"""
Home Assistant Sensor Extraction Script - Security Enhanced
Creates comprehensive sensor documentation with status and details
"""

import requests
import json
import csv
from datetime import datetime
import os
import yaml

# Configuration
HA_URL = "http://192.168.1.30:8123"

def load_secrets():
    """Load secrets from secrets.yaml file"""
    secrets_path = "/config/secrets.yaml"
    try:
        with open(secrets_path, 'r') as file:
            secrets = yaml.safe_load(file)
            return secrets.get('ha_long_lived_token')
    except Exception as e:
        print(f"❌ Error loading secrets: {e}")
        return None

# Load token securely from secrets
HA_TOKEN = load_secrets()
if not HA_TOKEN:
    print("❌ Error: Unable to load HA token from secrets.yaml")
    exit(1)

OUTPUT_DIR = "/config/sensor_reports"

# Headers for API requests
headers = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json"
}

def get_all_entities():
    """Get all entities from Home Assistant"""
    url = f"{HA_URL}/api/states"
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ API Error: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection Error: {e}")
        return []

def extract_sensor_info(entity):
    """Extract relevant sensor information"""
    attributes = entity.get('attributes', {})
    
    return {
        'Entity ID': entity.get('entity_id'),
        'Friendly Name': attributes.get('friendly_name', 'N/A'),
        'State': entity.get('state'),
        'Unit': attributes.get('unit_of_measurement', 'N/A'),
        'Device Class': attributes.get('device_class', 'N/A'),
        'State Class': attributes.get('state_class', 'N/A'),
        'Icon': attributes.get('icon', 'N/A'),
        'Last Updated': entity.get('last_updated'),
        'Last Changed': entity.get('last_changed'),
        'Domain': entity.get('entity_id', '').split('.')[0],
        'Integration': attributes.get('attribution', 'N/A'),
        'Restored': attributes.get('restored', False),
        'Supported Features': attributes.get('supported_features', 'N/A')
    }

def main():
    print("🔍 Starting Home Assistant Sensor Extraction...")
    print("🔐 Loading credentials securely...")
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Get all entities
    entities = get_all_entities()
    if not entities:
        print("❌ Failed to retrieve entities")
        return
    
    # Filter and process sensors
    sensors = [entity for entity in entities if entity.get('entity_id', '').startswith('sensor.')]
    binary_sensors = [entity for entity in entities if entity.get('entity_id', '').startswith('binary_sensor.')]
    
    # Generate timestamp for filenames
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Process all sensor data
    sensor_data = []
    for sensor in sensors + binary_sensors:
        sensor_info = extract_sensor_info(sensor)
        sensor_data.append(sensor_info)
    
    # Export to CSV
    csv_file = os.path.join(OUTPUT_DIR, f"sensors_report_{timestamp}.csv")
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        if sensor_data:
            writer = csv.DictWriter(file, fieldnames=sensor_data[0].keys())
            writer.writeheader()
            writer.writerows(sensor_data)
    
    print(f"   📊 CSV Export: {csv_file}")
    
    # Export to JSON
    json_file = os.path.join(OUTPUT_DIR, f"sensors_report_{timestamp}.json")
    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total_sensors': len(sensors),
            'total_binary_sensors': len(binary_sensors),
            'sensors': sensor_data
        }, file, indent=2, default=str)
    
    print(f"   📋 JSON Export: {json_file}")
    
    # Generate summary report
    summary_file = os.path.join(OUTPUT_DIR, f"sensors_summary_{timestamp}.md")
    
    # Group by integration for summary
    integrations = {}
    for sensor_info in sensor_data:
        integration = sensor_info['Integration']
        if integration not in integrations:
            integrations[integration] = []
        integrations[integration].append(sensor_info)
    
    with open(summary_file, 'w', encoding='utf-8') as file:
        file.write(f"# Home Assistant Sensor Summary Report\n\n")
        file.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        file.write(f"**Total Sensors:** {len(sensors)}\n")
        file.write(f"**Total Binary Sensors:** {len(binary_sensors)}\n")
        file.write(f"**Total Entities:** {len(sensors) + len(binary_sensors)}\n\n")
        
        file.write("## Sensors by Integration\n\n")
        for integration, entities in sorted(integrations.items()):
            file.write(f"### {integration}\n")
            file.write(f"**Count:** {len(entities)}\n\n")
            
            file.write("| Entity ID | Friendly Name | State | Unit | Status |\n")
            file.write("|-----------|---------------|-------|------|--------|\n")
            
            for entity in entities[:10]:  # Limit to first 10 per integration
                status = "✅ OK" if entity['State'] not in ['unknown', 'unavailable'] else "❌ Issue"
                file.write(f"| `{entity['Entity ID']}` | {entity['Friendly Name']} | {entity['State']} | {entity['Unit']} | {status} |\n")
            
            if len(entities) > 10:
                file.write(f"| ... | *{len(entities) - 10} more entities* | ... | ... | ... |\n")
            
            file.write("\n")
    
    print(f"   📄 Summary: {summary_file}")
    print(f"✅ Sensor extraction completed successfully!")
    print(f"📁 Reports saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()