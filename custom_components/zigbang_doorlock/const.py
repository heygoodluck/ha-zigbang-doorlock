DOMAIN = "zigbang_doorlock"
ATTR_BATTERY = "battery_level"
ATTR_LOCK_STATE = "lock_state"

# 언어별 알림 타입 정의 (기본 지원: 한국어, 영어)
ALERT_TYPE = {
    '622_NONE': 'locked',
    '622_IN_BLE': 'unlocked',
    '622_IN_FCE': 'unlocked',
    '622_IN_FGP': 'unlocked',
    '622_IN_MST': 'unlocked',
    '622_IN_NFC': 'unlocked',
    '622_IN_NUM': 'unlocked',
    '622_IN_RFC': 'unlocked',
    '622_IN_RMC': 'unlocked',
    '622_IN_SVR': 'unlocked',
    '622_IN_VCE': 'unlocked',
    '622_OUT': 'unlocked',
    '620': 'unlock_failed_5_times',
    '648': 'unlocked_for_30_seconds',
    '652': 'lock_failed'
}

UNLOCK_TOOL = {
    'BLE': {
        'name': 'bluetooth',
        'user_name_key': "pinNm"
    },
    'FCE': {
        'name': 'face',
        'user_name_key': "pinNm"
    },
    'FGP': {
        'name': 'fingerprint',
        'user_name_key': "pinNm"
    },
    'MST': {
        'name': 'mst',
        'user_name_key': "eventMemberNm"
    },
    'NFC': {
        'name': 'nfc',
        'user_name_key': "eventMemberNm"
    },
    'NUM': {
        'name': 'number',
        'user_name_key': None
    },
    'RFC': {
        'name': 'keytag',
        'user_name_key': "pinNm"
    },
    'RMC': {
        'name': 'remote_controller',
        'user_name_key': "pinNm"
    },
    'SVR': {
        'name': 'application',
        'user_name_key': "eventMemberNm"
    },
    'VCE': {
        'name': 'voice',
        'user_name_key': "pinNm"
    },
    'INDOOR': {
        'name': 'in_door_button',
        'user_name_key': None
    }
}
