import asyncio
from asyncio import Future

import pytest
from pytest_mock import MockFixture

from custom_components.ac_infinity.const import DOMAIN, PortControlKey
from custom_components.ac_infinity.switch import (
    SCHEDULE_DISABLED_VALUE,
    SCHEDULE_EOD_VALUE,
    SCHEDULE_MIDNIGHT_VALUE,
    ACInfinityPortSwitchEntity,
    async_setup_entry,
)
from tests import (
    ACTestObjects,
    execute_and_get_port_entity,
    setup_entity_mocks,
)
from tests.data_models import DEVICE_ID, MAC_ADDR


@pytest.fixture
def setup(mocker: MockFixture):
    return setup_entity_mocks(mocker)


@pytest.mark.asyncio
class TestSwitches:
    async def test_async_setup_all_sensors_created(self, setup):
        """All sensors created"""
        test_objects: ACTestObjects = setup

        await async_setup_entry(
            test_objects.hass,
            test_objects.config_entry,
            test_objects.entities.add_entities_callback,
        )

        assert len(test_objects.entities._added_entities) == 32

    @pytest.mark.parametrize(
        "setting",
        [
            PortControlKey.AUTO_HUMIDITY_HIGH_ENABLED,
            PortControlKey.AUTO_HUMIDITY_LOW_ENABLED,
            PortControlKey.AUTO_TEMP_HIGH_ENABLED,
            PortControlKey.AUTO_TEMP_LOW_ENABLED,
            PortControlKey.VPD_HIGH_ENABLED,
            PortControlKey.VPD_LOW_ENABLED,
            PortControlKey.SCHEDULED_START_TIME,
            PortControlKey.SCHEDULED_END_TIME,
        ],
    )
    @pytest.mark.parametrize("port", [1, 2, 3, 4])
    async def test_async_setup_mode_created_for_each_port(self, setup, port, setting):
        """Sensor for device port mode created on setup"""

        entity = await execute_and_get_port_entity(
            setup,
            async_setup_entry,
            port,
            setting,
        )

        assert entity.unique_id == f"{DOMAIN}_{MAC_ADDR}_port_{port}_{setting}"
        assert entity.device_info is not None

    @pytest.mark.parametrize(
        "setting,value,expected",
        [
            # enabled
            (PortControlKey.AUTO_HUMIDITY_HIGH_ENABLED, 1, True),
            (PortControlKey.AUTO_HUMIDITY_LOW_ENABLED, 1, True),
            (PortControlKey.AUTO_TEMP_HIGH_ENABLED, 1, True),
            (PortControlKey.AUTO_TEMP_LOW_ENABLED, 1, True),
            (PortControlKey.VPD_HIGH_ENABLED, 1, True),
            (PortControlKey.VPD_LOW_ENABLED, 1, True),
            (PortControlKey.SCHEDULED_START_TIME, SCHEDULE_MIDNIGHT_VALUE, True),
            (PortControlKey.SCHEDULED_END_TIME, SCHEDULE_MIDNIGHT_VALUE, True),
            # disabled
            (PortControlKey.AUTO_HUMIDITY_HIGH_ENABLED, 0, False),
            (PortControlKey.AUTO_HUMIDITY_LOW_ENABLED, 0, False),
            (PortControlKey.AUTO_TEMP_HIGH_ENABLED, 0, False),
            (PortControlKey.AUTO_TEMP_LOW_ENABLED, 0, False),
            (PortControlKey.VPD_HIGH_ENABLED, 0, False),
            (PortControlKey.VPD_LOW_ENABLED, 0, False),
            (PortControlKey.SCHEDULED_START_TIME, SCHEDULE_DISABLED_VALUE, False),
            (PortControlKey.SCHEDULED_END_TIME, SCHEDULE_DISABLED_VALUE, False),
        ],
    )
    @pytest.mark.parametrize("port", [1, 2, 3, 4])
    async def test_async_update_mode_value_correct(
        self, setup, setting, expected, port, value
    ):
        """Reported sensor value matches the value in the json payload"""

        test_objects: ACTestObjects = setup
        entity = await execute_and_get_port_entity(
            setup,
            async_setup_entry,
            port,
            setting,
        )

        test_objects.ac_infinity._port_controls[(str(DEVICE_ID), port)][setting] = value
        entity._handle_coordinator_update()

        assert isinstance(entity, ACInfinityPortSwitchEntity)
        assert entity.is_on == expected
        test_objects.write_ha_mock.assert_called()

    @pytest.mark.parametrize(
        "setting,expected",
        [
            # enabled
            (PortControlKey.AUTO_HUMIDITY_HIGH_ENABLED, 1),
            (PortControlKey.AUTO_HUMIDITY_LOW_ENABLED, 1),
            (PortControlKey.AUTO_TEMP_HIGH_ENABLED, 1),
            (PortControlKey.AUTO_TEMP_LOW_ENABLED, 1),
            (PortControlKey.VPD_HIGH_ENABLED, 1),
            (PortControlKey.VPD_LOW_ENABLED, 1),
            (PortControlKey.SCHEDULED_START_TIME, SCHEDULE_MIDNIGHT_VALUE),
            (PortControlKey.SCHEDULED_END_TIME, SCHEDULE_EOD_VALUE),
        ],
    )
    @pytest.mark.parametrize("port", [1, 2, 3, 4])
    async def test_async_turn_on(self, setup, expected, port, setting: str):
        """Reported sensor value matches the value in the json payload"""
        future: Future = asyncio.Future()
        future.set_result(None)

        test_objects: ACTestObjects = setup
        entity = await execute_and_get_port_entity(
            setup,
            async_setup_entry,
            port,
            setting,
        )

        assert isinstance(entity, ACInfinityPortSwitchEntity)
        await entity.async_turn_on()

        test_objects.port_set_mock.assert_called_with(
            str(DEVICE_ID), port, setting, expected
        )
        test_objects.refresh_mock.assert_called()

    @pytest.mark.parametrize(
        "setting,expected",
        [
            (PortControlKey.AUTO_HUMIDITY_HIGH_ENABLED, 0),
            (PortControlKey.AUTO_HUMIDITY_LOW_ENABLED, 0),
            (PortControlKey.AUTO_TEMP_HIGH_ENABLED, 0),
            (PortControlKey.AUTO_TEMP_LOW_ENABLED, 0),
            (PortControlKey.VPD_HIGH_ENABLED, 0),
            (PortControlKey.VPD_LOW_ENABLED, 0),
            (PortControlKey.SCHEDULED_START_TIME, SCHEDULE_DISABLED_VALUE),
            (PortControlKey.SCHEDULED_END_TIME, SCHEDULE_DISABLED_VALUE),
        ],
    )
    @pytest.mark.parametrize("port", [1, 2, 3, 4])
    async def test_async_turn_off(self, setup, expected, port, setting: str):
        """Reported sensor value matches the value in the json payload"""
        future: Future = asyncio.Future()
        future.set_result(None)

        test_objects: ACTestObjects = setup
        entity = await execute_and_get_port_entity(
            setup,
            async_setup_entry,
            port,
            setting,
        )

        assert isinstance(entity, ACInfinityPortSwitchEntity)
        await entity.async_turn_off()

        test_objects.port_set_mock.assert_called_with(
            str(DEVICE_ID), port, setting, expected
        )
        test_objects.refresh_mock.assert_called()
