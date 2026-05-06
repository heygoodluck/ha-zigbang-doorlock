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
    'BLE': 'bluetooth',
    'FCE': 'face',
    'FGP': 'fingerprint',
    'MST': 'mst',
    'NFC': 'nfc',
    'NUM': 'number',
    'RFC': 'keytag',
    'RMC': 'remote_controller',
    'SVR': 'application',
    'VCE': 'voice',
    'INDOOR': 'in_door_button',
    '622_IN_BLE': 'bluetooth',
    '622_IN_FCE': 'face',
    '622_IN_FGP': 'fingerprint',
    '622_IN_MST': 'mst',
    '622_IN_NFC': 'nfc',
    '622_IN_NUM': 'number',
    '622_IN_RFC': 'keytag',
    '622_IN_RMC': 'remote_controller',
    '622_IN_SVR': 'application',
    '622_IN_VCE': 'voice',
    '622_OUT': 'in_door',
}
