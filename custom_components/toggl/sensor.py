"""Platform for sensor integration."""
import logging
from datetime import datetime, date, timedelta
from homeassistant.components.sensor import ENTITY_ID_FORMAT
from homeassistant.helpers.entity import Entity, generate_entity_id
from homeassistant.helpers import entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.const import TIME_MILLISECONDS
from uuid import getnode as get_mac
from .const import DOMAIN, CONF_SENSOR


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Setup the sensor platform."""
    async_add_entities([TogglSensor(hass, discovery_info)], True)


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Setup sensor platform."""
    async_add_devices([TogglSensor(hass, config_entry.data)], True)


_LOGGER = logging.getLogger(__name__)


class TogglSensor(Entity):
    """Toggl Sensor class"""

    def __init__(self, hass, config):
        """Initialize the sensor."""
        self._state = None
        # self.config = config
        self.api = hass.data[DOMAIN]["toggl"]
        self.api.setAPIKey(config.get("token"))
        self._unit_of_measurement = TIME_MILLISECONDS
        self._name = "toggl"
        self._id_prefix = "toggl_"
        self._unique_id = "{}-{}-{}".format(get_mac(), CONF_SENSOR, self._name)
        self.entity_id = generate_entity_id(
            ENTITY_ID_FORMAT, self._id_prefix + self._name, []
        )

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": self.name,
            "manufacturer": "Toggl",
        }

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the name of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit this state is expressed in."""
        return self._unit_of_measurement

    @property
    def unique_id(self):
        """Return a unique ID to use for this sensor."""
        return self._unique_id

    async def async_update(self):
        """update the sensor"""
        ws = self.api.getWorkspaces()
        report_week = self.api.getWeeklyReport({"workspace_id": ws[0]["id"]})
        self._state = report_week["total_grand"]
