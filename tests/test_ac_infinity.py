import pytest
from homeassistant.helpers.update_coordinator import UpdateFailed
from pytest_mock import MockFixture
from pytest_mock.plugin import MockType

from custom_components.ac_infinity.ac_infinity import ACInfinity
from custom_components.ac_infinity.client import ACInfinityClient
from custom_components.ac_infinity.const import (
    DEVICE_KEY_DEVICE_NAME,
    DEVICE_KEY_HUMIDITY,
    DEVICE_KEY_MAC_ADDR,
    DEVICE_KEY_TEMPERATURE,
    DEVICE_PORT_KEY_NAME,
    DEVICE_PORT_KEY_SPEAK,
    DOMAIN,
    MANUFACTURER,
)

from .data_models import (
    DEVICE_ID,
    DEVICE_INFO_LIST_ALL,
    DEVICE_NAME,
    EMAIL,
    MAC_ADDR,
    PASSWORD,
)


@pytest.mark.asyncio
class TestACInfinity:
    async def test_update_logged_in_should_be_called_if_not_logged_in(
        self, mocker: MockFixture
    ):
        """if client is already logged in, than log in should not be called"""

        mocker.patch.object(ACInfinityClient, "is_logged_in", return_value=False)
        mocker.patch.object(
            ACInfinityClient, "get_all_device_info", return_value=DEVICE_INFO_LIST_ALL
        )
        mockLogin: MockType = mocker.patch.object(ACInfinityClient, "login")

        ac_infinity = ACInfinity(EMAIL, PASSWORD)
        await ac_infinity.update()

        assert mockLogin.called

    async def test_update_logged_in_should_not_be_called_if_not_necessary(
        self, mocker: MockFixture
    ):
        """if client is not already logged in, than log in should be called"""

        mocker.patch.object(ACInfinityClient, "is_logged_in", return_value=True)
        mocker.patch.object(
            ACInfinityClient, "get_all_device_info", return_value=DEVICE_INFO_LIST_ALL
        )
        mockLogin: MockType = mocker.patch.object(ACInfinityClient, "login")

        ac_infinity = ACInfinity(EMAIL, PASSWORD)
        await ac_infinity.update()
        assert not mockLogin.called

    async def test_update_data_set(self, mocker: MockFixture):
        """data should be set once update is called"""

        mocker.patch.object(ACInfinityClient, "is_logged_in", return_value=True)
        mocker.patch.object(
            ACInfinityClient, "get_all_device_info", return_value=DEVICE_INFO_LIST_ALL
        )
        mocker.patch.object(ACInfinityClient, "login")

        ac_infinity = ACInfinity(EMAIL, PASSWORD)
        await ac_infinity.update()

        assert len(ac_infinity._data) == 1
        assert ac_infinity._data[0][DEVICE_KEY_DEVICE_NAME] == "Grow Tent"

    @pytest.mark.parametrize(
        "property, value",
        [
            (DEVICE_KEY_DEVICE_NAME, "Grow Tent"),
            (DEVICE_KEY_MAC_ADDR, MAC_ADDR),
            (DEVICE_KEY_TEMPERATURE, 2417),
            (DEVICE_KEY_HUMIDITY, 7200),
        ],
    )
    @pytest.mark.parametrize("device_id", [DEVICE_ID, str(DEVICE_ID)])
    async def test_get_device_property_gets_correct_property(
        self, device_id, property, value
    ):
        """getting a device property returns the correct value"""
        ac_infinity = ACInfinity(EMAIL, PASSWORD)
        ac_infinity._data = DEVICE_INFO_LIST_ALL

        result = ac_infinity.get_device_property(device_id, property)
        assert result == value

    @pytest.mark.parametrize(
        "property, device_id",
        [
            (DEVICE_KEY_DEVICE_NAME, "232161"),
            ("MyFakeField", DEVICE_ID),
            ("MyFakeField", str(DEVICE_ID)),
        ],
    )
    async def test_get_device_property_returns_null_properly(self, property, device_id):
        """the absence of a value should return None instead of keyerror"""
        ac_infinity = ACInfinity(EMAIL, PASSWORD)
        ac_infinity._data = DEVICE_INFO_LIST_ALL

        result = ac_infinity.get_device_property(device_id, property)
        assert result is None

    @pytest.mark.parametrize(
        "property, port_num, value",
        [
            (DEVICE_PORT_KEY_SPEAK, 1, 5),
            (DEVICE_PORT_KEY_SPEAK, 2, 7),
            (DEVICE_PORT_KEY_NAME, 3, "Circulating Fan"),
            (DEVICE_PORT_KEY_NAME, 1, "Grow Lights"),
        ],
    )
    @pytest.mark.parametrize("device_id", [DEVICE_ID, str(DEVICE_ID)])
    async def test_get_device_port_property_gets_correct_property(
        self, device_id, port_num, property, value
    ):
        """getting a porp property gets the correct property from the correct port"""
        ac_infinity = ACInfinity(EMAIL, PASSWORD)
        ac_infinity._data = DEVICE_INFO_LIST_ALL

        result = ac_infinity.get_device_port_property(device_id, port_num, property)
        assert result == value

    @pytest.mark.parametrize(
        "property, device_id, port_num",
        [
            (DEVICE_PORT_KEY_SPEAK, "232161", 1),
            ("MyFakeField", DEVICE_ID, 1),
            (DEVICE_PORT_KEY_SPEAK, DEVICE_ID, 9),
            ("MyFakeField", str(DEVICE_ID), 1),
            (DEVICE_PORT_KEY_SPEAK, str(DEVICE_ID), 9),
        ],
    )
    async def test_get_device_port_property_returns_null_properly(
        self, property, device_id, port_num
    ):
        """the absence of a value should return None instead of keyerror"""
        ac_infinity = ACInfinity(EMAIL, PASSWORD)
        ac_infinity._data = DEVICE_INFO_LIST_ALL

        result = ac_infinity.get_device_port_property(device_id, port_num, property)
        assert result is None

    async def test_update_update_failed_thrown(self, mocker: MockFixture):
        mocker.patch.object(ACInfinityClient, "is_logged_in", return_value=True)
        mocker.patch.object(
            ACInfinityClient,
            "get_all_device_info",
            return_value=DEVICE_INFO_LIST_ALL,
            side_effect=Exception("unit test"),
        )
        mocker.patch.object(ACInfinityClient, "login")

        ac_infinity = ACInfinity(EMAIL, PASSWORD)
        with pytest.raises(UpdateFailed):
            await ac_infinity.update()

    async def test_get_device_all_device_meta_data_returns_meta_data(self):
        """getting port device ids should return ids"""
        ac_infinity = ACInfinity(EMAIL, PASSWORD)
        ac_infinity._data = DEVICE_INFO_LIST_ALL

        result = ac_infinity.get_all_device_meta_data()
        assert len(result) > 0

        device = result[0]
        assert device.device_id == str(DEVICE_ID)
        assert device.device_name == DEVICE_NAME
        assert device.mac_addr == MAC_ADDR
        assert [port.port_id for port in device.ports] == [1, 2, 3, 4]

    @pytest.mark.parametrize("data", [[], None])
    async def test_get_device_all_device_meta_data_returns_empty_list(self, data):
        """getting device metadata returns empty list if no device exists or data isn't initialized"""
        ac_infinity = ACInfinity(EMAIL, PASSWORD)
        ac_infinity._data = data

        result = ac_infinity.get_all_device_meta_data()
        assert result == []

    @pytest.mark.parametrize(
        "devType,expected_model",
        [(11, "Controller 69 Pro (CTR69P)"), (3, "Controller Type 3")],
    )
    async def test_ac_infinity_device_has_correct_device_info(
        self, devType: int, expected_model: str
    ):
        """getting device returns an model object that contains correct device info for the device registry"""
        ac_infinity = ACInfinity(EMAIL, PASSWORD)
        ac_infinity._data = DEVICE_INFO_LIST_ALL
        ac_infinity._data[0]["devType"] = devType

        result = ac_infinity.get_all_device_meta_data()
        assert len(result) > 0

        device = result[0]
        device_info = device._device_info
        assert (DOMAIN, str(DEVICE_ID)) in device_info.get("identifiers")
        assert device_info.get("hw_version") == "1.1"
        assert device_info.get("sw_version") == "3.2.25"
        assert device_info.get("name") == DEVICE_NAME
        assert device_info.get("manufacturer") == MANUFACTURER
        assert device_info.get("model") == expected_model
