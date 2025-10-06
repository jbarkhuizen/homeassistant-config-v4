import logging

import voluptuous as vol

from homeassistant import auth
from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_TOKEN, CONF_URL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.network import get_url

from . import _retrieve_access_token
from .const import CONF_REFRESH_TOKEN_ID, DOMAIN
from .exceptions import WebSocketAuthenticationError
from .ha_connection import HAConnection

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_TOKEN): str,
        vol.Optional(CONF_URL): str,
    }
)

DEVTOOLS_USER_NAME = "Developer Tools"
DEVTOOLS_CLIENT_NAME = "DevTools"


async def validate_input(hass: HomeAssistant, data: dict[str, any]):
    """Validate if the given token allows us to connect."""
    access_token = _retrieve_access_token(hass, data)

    async with HAConnection(
        url=data[CONF_URL],
        token=access_token,
        hass=hass,
        session=async_get_clientsession(hass),
    ) as sock:
        await sock.send_and_receive({"type": "ping"})


class DevToolsConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for devtools."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is None:
            return self._show_setup_form()

        token = user_input.get(CONF_TOKEN, "")
        url = user_input.get(CONF_URL, "")
        if url and not token:
            return self._show_setup_form({"base": "token_required_with_url"})

        if not url:
            url = get_url(self.hass)
            user_input[CONF_URL] = url
        if not token:
            refresh_token = await self._generate_refresh_token()
            user_input[CONF_REFRESH_TOKEN_ID] = refresh_token.id
            _LOGGER.debug("Generated refresh token: %s", refresh_token)

        try:
            await validate_input(self.hass, user_input)
        except WebSocketAuthenticationError:
            return self._show_setup_form({"base": "cannot_connect"})

        return self.async_create_entry(title="DevTools", data=user_input)

    def _show_setup_form(self, errors: dict | None = None):
        """Show the setup form to the user."""
        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors or {},
        )

    async def _generate_refresh_token(self) -> auth.models.RefreshToken:
        """Generate system user and refresh token."""

        user = await self.hass.auth.async_create_system_user(
            DEVTOOLS_USER_NAME, group_ids=[auth.const.GROUP_ID_ADMIN]
        )

        return await self.hass.auth.async_create_refresh_token(
            user=user,
            client_name=DEVTOOLS_CLIENT_NAME,
        )
