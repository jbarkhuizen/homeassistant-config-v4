#===============================================================================
# HOME ASSISTANT UPDATE SUMMARY SENSOR
# File: sensors/update_summary.yaml
# Updated: 2025-10-15
# Description: Monitors and reports on all available Home Assistant updates
#              Uses modern template sensor format
#===============================================================================

template:
  - sensor:
      #-------------------------------------------------------------------------
      # Main Update Summary Sensor
      #-------------------------------------------------------------------------
      - name: "Home Assistant Updates Summary"
        unique_id: home_assistant_updates_summary
        icon: mdi:package-up
        state: >
          {% set ns = namespace(updates=[]) %}
          
          {# Check Home Assistant Core Updates #}
          {% if states('update.home_assistant_core_update') == 'on' %}
            {% set ns.updates = ns.updates + ['Home Assistant Core'] %}
          {% endif %}
          
          {# Check Home Assistant Supervisor Updates #}
          {% if states('update.home_assistant_supervisor_update') == 'on' %}
            {% set ns.updates = ns.updates + ['Home Assistant Supervisor'] %}
          {% endif %}
          
          {# Check Home Assistant Operating System Updates #}
          {% if states('update.home_assistant_operating_system_update') == 'on' %}
            {% set ns.updates = ns.updates + ['Home Assistant OS'] %}
          {% endif %}
          
          {# Check all other update entities #}
          {% for entity in states.update %}
            {% if entity.state == 'on' and not entity.entity_id.startswith('update.home_assistant') %}
              {% set ns.updates = ns.updates + [entity.name] %}
            {% endif %}
          {% endfor %}
          
          {# Return result #}
          {% if ns.updates | length > 0 %}
            {{ ns.updates | join(', ') }}
          {% else %}
            No updates available
          {% endif %}
        
        availability: >
          {{ states('update.home_assistant_core_update') not in ['unavailable', 'unknown'] }}
        
        attributes:
          #---------------------------------------------------------------------
          # Total Update Count
          #---------------------------------------------------------------------
          total_updates: >
            {% set ns = namespace(count=0) %}
            
            {% if states('update.home_assistant_core_update') == 'on' %}
              {% set ns.count = ns.count + 1 %}
            {% endif %}
            
            {% if states('update.home_assistant_supervisor_update') == 'on' %}
              {% set ns.count = ns.count + 1 %}
            {% endif %}
            
            {% if states('update.home_assistant_operating_system_update') == 'on' %}
              {% set ns.count = ns.count + 1 %}
            {% endif %}
            
            {% for entity in states.update %}
              {% if entity.state == 'on' and not entity.entity_id.startswith('update.home_assistant') %}
                {% set ns.count = ns.count + 1 %}
              {% endif %}
            {% endfor %}
            
            {{ ns.count }}
          
          #---------------------------------------------------------------------
          # Updates List (Array Format)
          #---------------------------------------------------------------------
          updates_list: >
            {% set ns = namespace(list=[]) %}
            
            {% if states('update.home_assistant_core_update') == 'on' %}
              {% set ns.list = ns.list + ['Home Assistant Core'] %}
            {% endif %}
            
            {% if states('update.home_assistant_supervisor_update') == 'on' %}
              {% set ns.list = ns.list + ['Home Assistant Supervisor'] %}
            {% endif %}
            
            {% if states('update.home_assistant_operating_system_update') == 'on' %}
              {% set ns.list = ns.list + ['Home Assistant OS'] %}
            {% endif %}
            
            {% for entity in states.update %}
              {% if entity.state == 'on' and not entity.entity_id.startswith('update.home_assistant') %}
                {% set ns.list = ns.list + [entity.name] %}
              {% endif %}
            {% endfor %}
            
            {{ ns.list }}
          
          #---------------------------------------------------------------------
          # Detailed Status with Version Information
          #---------------------------------------------------------------------
          detailed_status: >
            {% set ns = namespace(details={}) %}
            
            {# Home Assistant Core #}
            {% if states('update.home_assistant_core_update') not in ['unavailable', 'unknown'] %}
              {% set current_version = state_attr('update.home_assistant_core_update', 'installed_version') | default('Unknown') %}
              {% set latest_version = state_attr('update.home_assistant_core_update', 'latest_version') | default('Unknown') %}
              {% set status = states('update.home_assistant_core_update') %}
              {% set ns.details = dict(ns.details, **{
                'Home Assistant Core': {
                  'status': status,
                  'current_version': current_version,
                  'latest_version': latest_version,
                  'update_available': status == 'on'
                }
              }) %}
            {% endif %}
            
            {# Home Assistant Supervisor #}
            {% if states('update.home_assistant_supervisor_update') not in ['unavailable', 'unknown'] %}
              {% set current_version = state_attr('update.home_assistant_supervisor_update', 'installed_version') | default('Unknown') %}
              {% set latest_version = state_attr('update.home_assistant_supervisor_update', 'latest_version') | default('Unknown') %}
              {% set status = states('update.home_assistant_supervisor_update') %}
              {% set ns.details = dict(ns.details, **{
                'Home Assistant Supervisor': {
                  'status': status,
                  'current_version': current_version,
                  'latest_version': latest_version,
                  'update_available': status == 'on'
                }
              }) %}
            {% endif %}
            
            {# Home Assistant OS #}
            {% if states('update.home_assistant_operating_system_update') not in ['unavailable', 'unknown'] %}
              {% set current_version = state_attr('update.home_assistant_operating_system_update', 'installed_version') | default('Unknown') %}
              {% set latest_version = state_attr('update.home_assistant_operating_system_update', 'latest_version') | default('Unknown') %}
              {% set status = states('update.home_assistant_operating_system_update') %}
              {% set ns.details = dict(ns.details, **{
                'Home Assistant OS': {
                  'status': status,
                  'current_version': current_version,
                  'latest_version': latest_version,
                  'update_available': status == 'on'
                }
              }) %}
            {% endif %}
            
            {# All Other Updates (Add-ons, HACS, Custom Components) #}
            {% for entity in states.update %}
              {% if not entity.entity_id.startswith('update.home_assistant') and entity.state not in ['unavailable', 'unknown'] %}
                {% set current_version = state_attr(entity.entity_id, 'installed_version') | default('Unknown') %}
                {% set latest_version = state_attr(entity.entity_id, 'latest_version') | default('Unknown') %}
                {% set status = entity.state %}
                {% set ns.details = dict(ns.details, **{
                  entity.name: {
                    'status': status,
                    'current_version': current_version,
                    'latest_version': latest_version,
                    'update_available': status == 'on',
                    'entity_id': entity.entity_id
                  }
                }) %}
              {% endif %}
            {% endfor %}
            
            {{ ns.details }}
          
          #---------------------------------------------------------------------
          # Critical Updates Flag
          #---------------------------------------------------------------------
          has_critical_updates: >
            {% set critical = states('update.home_assistant_core_update') == 'on' or 
                              states('update.home_assistant_supervisor_update') == 'on' or 
                              states('update.home_assistant_operating_system_update') == 'on' %}
            {{ critical }}
          
          #---------------------------------------------------------------------
          # Add-on Updates Count
          #---------------------------------------------------------------------
          addon_updates: >
            {% set ns = namespace(count=0) %}
            {% for entity in states.update %}
              {% if entity.state == 'on' and not entity.entity_id.startswith('update.home_assistant') %}
                {% set ns.count = ns.count + 1 %}
              {% endif %}
            {% endfor %}
            {{ ns.count }}
          
          #---------------------------------------------------------------------
          # Last Update Check Time
          #---------------------------------------------------------------------
          last_checked: >
            {{ now().strftime('%Y-%m-%d %H:%M:%S') }}
          
          #---------------------------------------------------------------------
          # Friendly Summary Message
          #---------------------------------------------------------------------
          friendly_summary: >
            {% set ns = namespace(updates=[]) %}
            
            {% if states('update.home_assistant_core_update') == 'on' %}
              {% set ns.updates = ns.updates + ['Core'] %}
            {% endif %}
            
            {% if states('update.home_assistant_supervisor_update') == 'on' %}
              {% set ns.updates = ns.updates + ['Supervisor'] %}
            {% endif %}
            
            {% if states('update.home_assistant_operating_system_update') == 'on' %}
              {% set ns.updates = ns.updates + ['OS'] %}
            {% endif %}
            
            {% set addon_count = namespace(count=0) %}
            {% for entity in states.update %}
              {% if entity.state == 'on' and not entity.entity_id.startswith('update.home_assistant') %}
                {% set addon_count.count = addon_count.count + 1 %}
              {% endif %}
            {% endfor %}
            
            {% if ns.updates | length == 0 and addon_count.count == 0 %}
              All systems up to date! ✅
            {% elif ns.updates | length > 0 and addon_count.count == 0 %}
              {{ ns.updates | join(', ') }} update(s) available
            {% elif ns.updates | length == 0 and addon_count.count > 0 %}
              {{ addon_count.count }} add-on update(s) available
            {% else %}
              {{ ns.updates | join(', ') }} and {{ addon_count.count }} add-on update(s) available
            {% endif %}

#===============================================================================
# BINARY SENSOR - Update Available Alert
#===============================================================================
  - binary_sensor:
      - name: "Updates Available"
        unique_id: updates_available_binary
        device_class: update
        icon: >
          {% if is_state('binary_sensor.updates_available', 'on') %}
            mdi:package-down
          {% else %}
            mdi:package-check
          {% endif %}
        state: >
          {% set core = states('update.home_assistant_core_update') == 'on' %}
          {% set supervisor = states('update.home_assistant_supervisor_update') == 'on' %}
          {% set os = states('update.home_assistant_operating_system_update') == 'on' %}
          
          {% set addon_updates = namespace(found=false) %}
          {% for entity in states.update %}
            {% if entity.state == 'on' and not entity.entity_id.startswith('update.home_assistant') %}
              {% set addon_updates.found = true %}
            {% endif %}
          {% endfor %}
          
          {{ core or supervisor or os or addon_updates.found }}
        
        attributes:
          update_type: >
            {% if states('update.home_assistant_core_update') == 'on' %}
              critical
            {% elif states('update.home_assistant_supervisor_update') == 'on' or states('update.home_assistant_operating_system_update') == 'on' %}
              important
            {% else %}
              normal
            {% endif %}

#===============================================================================
# END OF UPDATE SUMMARY CONFIGURATION
#===============================================================================