"""Constants for the AC Infinity integration."""

from homeassistant.const import Platform

MANUFACTURER = "AC Infinity"
DOMAIN = "ac_infinity"
PLATFORMS = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.SELECT,
    Platform.NUMBER,
    Platform.TIME,
    Platform.TEXT,
]
HOST = "http://www.acinfinityserver.com"

# devInfoListAll ReadOnly Device Fields
PROPERTY_KEY_DEVICE_ID = "devId"
PROPERTY_KEY_DEVICE_NAME = "devName"
PROPERTY_KEY_MAC_ADDR = "devMacAddr"
PROPERTY_KEY_DEVICE_INFO = "deviceInfo"
PROPERTY_KEY_PORTS = "ports"
PROPERTY_KEY_HW_VERSION = "hardwareVersion"
PROPERTY_KEY_SW_VERSION = "firmwareVersion"
PROPERTY_KEY_DEVICE_TYPE = "devType"
PROPERTY_PORT_KEY_PORT = "port"
PROPERTY_PORT_KEY_NAME = "portName"

# devInfoListAll Sensor State Fields
SENSOR_KEY_TEMPERATURE = "temperature"
SENSOR_KEY_HUMIDITY = "humidity"
SENSOR_KEY_VPD = "vpdnums"
SENSOR_PORT_KEY_SPEAK = "speak"
SENSOR_PORT_KEY_ONLINE = "online"

# getdevModeSettingsList Sensor Fields
SENSOR_SETTING_KEY_SURPLUS = "surplus"

# getdevModeSettingList Setting Fields
SETTING_KEY_ON_SPEED = "onSpead"
SETTING_KEY_OFF_SPEED = "offSpead"
SETTING_KEY_AT_TYPE = "atType"
SETTING_KEY_SCHEDULED_START_TIME = "schedStartTime"
SETTING_KEY_SCHEDULED_END_TIME = "schedEndtTime"
SETTING_KEY_ACTIVE_TIMER_ON = "acitveTimerOn"
SETTING_KEY_ACTIVE_TIMER_OFF = "acitveTimerOff"
