from datetime import timedelta
from typing import Any

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import UpdateFailed
from homeassistant.util import Throttle

from .client import ACInfinityClient
from .const import (
    DEVICE_KEY_DEVICE_ID,
    DEVICE_KEY_DEVICE_INFO,
    DEVICE_KEY_DEVICE_NAME,
    DEVICE_KEY_DEVICE_TYPE,
    DEVICE_KEY_HW_VERSION,
    DEVICE_KEY_MAC_ADDR,
    DEVICE_KEY_PORTS,
    DEVICE_KEY_SW_VERSION,
    DEVICE_PORT_KEY_NAME,
    DEVICE_PORT_KEY_PORT,
    DOMAIN,
    HOST,
    MANUFACTURER,
)


class ACInfinityDevice:
    def __init__(self, device_json) -> None:
        # device info
        self._device_id = str(device_json[DEVICE_KEY_DEVICE_ID])
        self._mac_addr = device_json[DEVICE_KEY_MAC_ADDR]
        self._device_name = device_json[DEVICE_KEY_DEVICE_NAME]
        self._identifier = (DOMAIN, self._device_id)
        self._ports = [
            ACInfinityDevicePort(self, port)
            for port in device_json[DEVICE_KEY_DEVICE_INFO][DEVICE_KEY_PORTS]
        ]

        self._device_info = DeviceInfo(
            identifiers={self._identifier},
            name=self._device_name,
            manufacturer=MANUFACTURER,
            hw_version=device_json[DEVICE_KEY_HW_VERSION],
            sw_version=device_json[DEVICE_KEY_SW_VERSION],
            model=self.__get_device_model_by_device_type(
                device_json[DEVICE_KEY_DEVICE_TYPE]
            ),
        )

    @property
    def device_id(self):
        return self._device_id

    @property
    def device_name(self):
        return self._device_name

    @property
    def mac_addr(self):
        return self._mac_addr

    @property
    def ports(self):
        return self._ports

    @property
    def device_info(self):
        return self._device_info

    @property
    def identifier(self):
        return self._identifier

    def __get_device_model_by_device_type(self, device_type: int):
        match device_type:
            case 11:
                return "UIS Controller 69 Pro (CTR69P)"
            case _:
                return f"UIS Controller Type {device_type}"


class ACInfinityDevicePort:
    def __init__(self, device: ACInfinityDevice, device_port_json) -> None:
        self._port_id = device_port_json[DEVICE_PORT_KEY_PORT]
        self._port_name = device_port_json[DEVICE_PORT_KEY_NAME]

        self._device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{device._device_id}_{self._port_id}")},
            name=f"{device._device_name} {self._port_name}",
            manufacturer=MANUFACTURER,
            via_device=device.identifier,
            model="UIS Enabled Device",
        )

    @property
    def port_id(self):
        return self._port_id

    @property
    def port_name(self):
        return self._port_name

    @property
    def device_info(self):
        return self._device_info


class ACInfinity:
    MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=5)

    def __init__(self, email: str, password: str) -> None:
        self._client = ACInfinityClient(HOST, email, password)
        self._devices: dict[str, dict[str, Any]] = {}
        self._port_settings: dict[str, dict[int, Any]] = {}

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def update(self):
        try:
            if not self._client.is_logged_in():
                await self._client.login()

            device_list = await self._client.get_all_device_info()
            for device in device_list:
                device_id = device[DEVICE_KEY_DEVICE_ID]
                self._devices[device_id] = device
                self._port_settings[device_id] = {}
                for port in device[DEVICE_KEY_DEVICE_INFO][DEVICE_KEY_PORTS]:
                    port_id = port[DEVICE_PORT_KEY_PORT]
                    self._port_settings[device_id][
                        port_id
                    ] = await self._client.get_device_port_settings(device_id, port_id)

        except Exception:
            raise UpdateFailed from Exception

    def get_all_device_meta_data(self) -> list[ACInfinityDevice]:
        """gets device metadata, such as ids, labels, macaddr, etc.. that are not expected to change"""
        if (self._devices) is None:
            return []

        return [ACInfinityDevice(device) for device in self._devices.values()]

    def get_device_port_setting(
        self, device_id: (str | int), port_id: int, setting: str
    ):
        if (
            device_id in self._port_settings
            and port_id in self._port_settings[device_id]
            and setting in self._port_settings[device_id][port_id]
        ):
            return self._port_settings[device_id][port_id][setting]

        return None

    async def set_device_port_setting(
        self, device_id: (str | int), port_id: int, setting: str, value: str
    ):
        await self._client.set_device_port_setting(device_id, port_id, setting, value)

    def get_device_property(self, device_id: (str | int), property_key: str):
        """gets a property, if it exists, from a given device, if it exists"""
        if str(device_id) in self._devices:
            result = self._devices[str(device_id)]
            if property_key in result:
                return result[property_key]
            elif property_key in result[DEVICE_KEY_DEVICE_INFO]:
                return result[DEVICE_KEY_DEVICE_INFO][property_key]

        return None

    def get_device_port_property(
        self, device_id: (str | int), port_id: int, property_key: str
    ):
        """gets a property, if it exists, from the given port, if it exists,  from the given device, if it exists"""
        if str(device_id) in self._devices:
            device = self._devices[str(device_id)]
            result = next(
                (
                    port
                    for port in device[DEVICE_KEY_DEVICE_INFO][DEVICE_KEY_PORTS]
                    if port[DEVICE_PORT_KEY_PORT] == port_id
                ),
                None,
            )

            if result is not None and property_key in result:
                return result[property_key]

        return None
