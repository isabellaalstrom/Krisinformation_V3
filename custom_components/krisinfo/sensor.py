from homeassistant.util import Throttle
from datetime import timedelta

from .device import KRISDevice
from .const import INTEGRATION_DOMAIN, CONF_NAME, CONF_INTEGRATION_ID

import logging


async def async_setup_entry(hass, config, async_add_devices):

    if not INTEGRATION_DOMAIN in hass.data:
        return False

    async_add_devices(
        [
            KrisinformationNewsSensor(
                hass.data[INTEGRATION_DOMAIN]["api"],
                config.title,
                config.data[CONF_INTEGRATION_ID],
            ),
            KrisinformationVMASensor(
                hass.data[INTEGRATION_DOMAIN]["api"],
                config.title,
                config.data[CONF_INTEGRATION_ID],
            ),
        ]
    )


class KrisinformationVMASensor(KRISDevice):
    """Representation of a Krisinformation VMA sensor."""

    def __init__(self, api, name, id):
        """Initialize a Krisinformation sensor."""
        self._api = api
        self._name = name
        self._id = id
        self._icon = "mdi:alert-outline"
        self.logger = logging.getLogger(INTEGRATION_DOMAIN)

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._name} VMA Sensor"

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        if not self._api.available:
            return "mdi:close-circle-outline"

        if "display_icon" in self._api.attributes:
            return self._api.attributes["display_icon"]

        return self._icon

    @property
    def state(self):
        """Return the state of the device."""
        return self._api.data["state"]

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the sensor."""
        self.logger.debug("ATTRIBUTES")

        return self._api.attributes

    @property
    def available(self):
        """Could the device be accessed during the last update call."""
        return self._api.available

    @Throttle(timedelta(minutes=5))
    async def async_update(self):
        """Get the latest data from the Krisinformation API."""
        await self._api.updateVmas()

    @property
    def device_class(self):
        """Return the class of this device."""
        return "problem"

    @property
    def should_poll(self):
        """No polling needed."""
        return True

    @property
    def unique_id(self):
        return f"kris-{self._id}-vma-sensor"


class KrisinformationNewsSensor(KRISDevice):
    """Representation of a Krisinformation news sensor."""

    def __init__(self, api, name, id):
        """Initialize a Krisinformation sensor."""
        self._api = api
        self._name = name
        self._id = id
        self._icon = "mdi:alert-outline"
        self.logger = logging.getLogger(INTEGRATION_DOMAIN)

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._name} News Sensor"

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        if not self._api.available:
            return "mdi:close-circle-outline"

        if "display_icon" in self._api.attributes:
            return self._api.attributes["display_icon"]

        return self._icon

    @property
    def state(self):
        """Return the state of the device."""
        return self._api.data["state"]

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the sensor."""
        self.logger.debug("ATTRIBUTES")

        return self._api.attributes

    @property
    def available(self):
        """Could the device be accessed during the last update call."""
        return self._api.available

    @Throttle(timedelta(minutes=5))
    async def async_update(self):
        """Get the latest data from the Krisinformation API."""
        await self._api.updateNews()

    @property
    def device_class(self):
        """Return the class of this device."""
        return "problem"

    @property
    def should_poll(self):
        """No polling needed."""
        return True

    @property
    def unique_id(self):
        return f"kris-{self._id}-news-sensor"
