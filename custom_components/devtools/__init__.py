import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_TOKEN, CONF_URL
from homeassistant.core import (
    HomeAssistant,
    ServiceCall,
    ServiceResponse,
    SupportsResponse,
)
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_REFRESH_TOKEN_ID, DOMAIN
from .ha_connection import HAConnection

_LOGGER = logging.getLogger(__package__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up devtools from a config entry."""
    url = entry.data[CONF_URL]
    web_session = async_get_clientsession(hass)

    async def handle_call_ws_endpoint(call: ServiceCall) -> ServiceResponse:
        ws_type = call.data.get("type")
        ws_data = call.data.get("data", {})
        access_token = _retrieve_access_token(call.hass, entry.data)

        message = {"type": ws_type, **ws_data}
        async with HAConnection(
            url=url,
            token=access_token,
            hass=call.hass,
            session=web_session,
        ) as sock:
            response = await sock.send_and_receive(message)
            if call.return_response:
                return {
                    "response": response,
                }
            return None

    hass.services.async_register(
        DOMAIN,
        "call_ws_endpoint",
        handle_call_ws_endpoint,
        supports_response=SupportsResponse.OPTIONAL,
    )

    return True


def _retrieve_access_token(hass: HomeAssistant, data) -> str:
    """Retrieve access token from config entry data."""
    access_token = data.get(CONF_TOKEN)
    refresh_token_id = data.get(CONF_REFRESH_TOKEN_ID)
    if refresh_token_id is not None:
        refresh_token = hass.auth.async_get_refresh_token(refresh_token_id)
        access_token = hass.auth.async_create_access_token(refresh_token)
    return access_token
