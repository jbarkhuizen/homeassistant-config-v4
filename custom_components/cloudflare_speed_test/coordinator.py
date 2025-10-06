"""Coordinator for cloudflare_speed_test."""

from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any, cast

from cfspeedtest import CloudflareSpeedtest

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DEFAULT_SPEED_TEST_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)

type CloudflareSpeedTestConfigEntry = ConfigEntry[CloudflareSpeedTestDataCoordinator]


class CloudflareSpeedTestDataCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Get the latest data from Cloudflare Speed Test."""

    config_entry: CloudflareSpeedTestConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: CloudflareSpeedTestConfigEntry,
        api: CloudflareSpeedtest,
        *,
        speed_test_interval_minutes: int | None = None,
    ) -> None:
        """Initialize the data object."""
        self.hass = hass
        self.api = api()

        minutes = speed_test_interval_minutes or DEFAULT_SPEED_TEST_INTERVAL

        super().__init__(
            self.hass,
            _LOGGER,
            config_entry=config_entry,
            name=DOMAIN,
            update_interval=timedelta(minutes=minutes),
        )

    def update_data(self) -> dict[str, Any]:
        """Get the latest data from Cloudflare Speed Test."""
        results = self.api.run_all()
        return cast(dict[str, Any], results)

    async def _async_update_data(self) -> dict[str, Any]:
        """Update CloudflareSpeedTest data."""
        return await self.hass.async_add_executor_job(self.update_data)
