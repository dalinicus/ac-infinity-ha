HOST = "https://unittest.abcxyz"
EMAIL = "myemail@unittest.com"
PASSWORD = "hunter2"

USER_ID = "11763238626156107487"
DEVICE_ID = 54929097239553773072
DEVICE_NAME = "Grow Tent"
MAC_ADDR = "2B120D62DC00"

LOGIN_PAYLOAD = {
    "msg": "Success",
    "code": 200,
    "data": {
        "appId": USER_ID,
        "nickName": EMAIL,
        "appEmail": EMAIL,
        "appPasswordl": "286519e4331f486cbbef02180f5e2f",
        "appUsable": 1,
        "forumUsable": 1,
        "forumRole": 0,
        "appCreateTime": "2023-07-11 20:59:07",
        "appIsanalytics": 0,
        "appIsbugreport": 0,
        "appIsemailrepost": 0,
        "createTime": None,
    },
}

DEVICE_INFO_LIST_ALL = [
    {
        "devId": str(DEVICE_ID),
        "devCode": "ABCDEFG",
        "devName": DEVICE_NAME,
        "devType": 11,
        "devAccesstime": 1692328784,
        "devPortCount": 4,
        "devOfftime": 1692328718,
        "devMacAddr": MAC_ADDR,
        "devVersion": 7,
        "online": 1,
        "isShare": 0,
        "devExternalList": None,
        "deviceInfo": {
            "devId": DEVICE_ID,
            "temperature": 2417,
            "temperatureF": 7551,
            "humidity": 7200,
            "tTrend": 0,
            "hTrend": 0,
            "unit": 0,
            "speak": 0,
            "trend": 0,
            "curMode": 3,
            "remainTime": None,
            "modeTye": 15,
            "advTriggerInfo": None,
            "notificationTrigger": None,
            "alertTrigger": None,
            "online": 1,
            "lkType": None,
            "endTime": 1692328718,
            "master": 0,
            "masterPort": 2,
            "allPortStatus": 7,
            "ports": [
                {
                    "speak": 5,
                    "deviceType": None,
                    "trend": 0,
                    "port": 1,
                    "curMode": 7,
                    "remainTime": 46545,
                    "modeTye": 0,
                    "online": 1,
                    "portName": "Grow Lights",
                    "portAccess": None,
                    "portResistance": 3300,
                    "isOpenAutomation": 0,
                    "advUpdateTime": None,
                    "loadType": 0,
                    "loadState": 1,
                    "abnormalState": 0,
                    "overcurrentStatus": 0,
                },
                {
                    "speak": 7,
                    "deviceType": None,
                    "trend": 0,
                    "port": 2,
                    "curMode": 2,
                    "remainTime": None,
                    "modeTye": 15,
                    "online": 1,
                    "portName": "Exhaust Fan",
                    "portAccess": None,
                    "portResistance": 5100,
                    "isOpenAutomation": 0,
                    "advUpdateTime": None,
                    "loadType": 0,
                    "loadState": 1,
                    "abnormalState": 0,
                    "overcurrentStatus": 0,
                },
                {
                    "speak": 5,
                    "deviceType": None,
                    "trend": 0,
                    "port": 3,
                    "curMode": 2,
                    "remainTime": None,
                    "modeTye": 15,
                    "online": 1,
                    "portName": "Circulating Fan",
                    "portAccess": None,
                    "portResistance": 10000,
                    "isOpenAutomation": 0,
                    "advUpdateTime": None,
                    "loadType": 0,
                    "loadState": 1,
                    "abnormalState": 0,
                    "overcurrentStatus": 0,
                },
                {
                    "speak": 0,
                    "deviceType": None,
                    "trend": 0,
                    "port": 4,
                    "curMode": 2,
                    "remainTime": None,
                    "modeTye": 15,
                    "online": 0,
                    "portName": "Port 4",
                    "portAccess": None,
                    "portResistance": 65535,
                    "isOpenAutomation": 0,
                    "advUpdateTime": None,
                    "loadType": 0,
                    "loadState": 0,
                    "abnormalState": 0,
                    "overcurrentStatus": 0,
                },
            ],
            "logCreateTime": None,
            "isOpenAutomation": 0,
            "advUpdateTime": None,
            "loadState": 0,
            "abnormalState": 0,
            "deviceInfoI": None,
            "tempCompare": 0,
            "humiCompare": 0,
            "ectdsType": None,
            "tdsUnit": None,
            "ecUnit": None,
            "sensorCount": None,
            "sensors": None,
            "overcurrentStatus": 0,
            "vpdnums": 83,
            "vpdstatus": 0,
        },
        "appEmail": EMAIL,
        "devTimeZone": "GMT+00:00",
        "createTime": None,
        "timeGMT": None,
        "timeZone": None,
        "firmwareVersion": "3.2.25",
        "hardwareVersion": "1.1",
        "workMode": 1,
        "zoneId": "America/Chicago",
        "wifiName": None,
    }
]

DEVICE_INFO_LIST_ALL_PAYLOAD = {
    "msg": "操作成功",
    "code": 200,
    "data": DEVICE_INFO_LIST_ALL,
}
