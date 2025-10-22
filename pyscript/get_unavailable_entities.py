# Get all unavailable entities
unavailable = []
for entity in hass.states.async_all():
    if entity.state in ['unavailable', 'unknown']:
        unavailable.append({
            'entity_id': entity.entity_id,
            'friendly_name': entity.attributes.get('friendly_name', entity.entity_id),
            'state': entity.state
        })

# Return results
unavailable.sort(key=lambda x: x['entity_id'])
hass.services.call('python_script', 'set_state', {
    'entity_id': 'sensor.unavailable_entities_count',
    'state': len(unavailable),
    'attributes': {
        'entities': unavailable
    }
})