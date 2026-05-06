DOMAIN = "zigbang_doorlock"
ATTR_BATTERY = "battery_level"
ATTR_LOCK_STATE = "lock_state"

# 언어별 알림 타입 정의 (기본 지원: 한국어, 영어)
ALERT_TYPE = {
    '622_NONE': 'locked',
    '622_IN_FGP': 'unlocked',
    '622_IN_RFC': 'unlocked',
    '622_OUT': 'unlocked',
    '622_IN_SVR': 'unlocked',
    '620': 'unlock_failed_5_times',
    '648': 'unlocked_for_30_seconds',
    '652': 'lock_failed'
}

UNLOCK_TOOL = {
    'FGP': 'fingerprint',
    'SVR': 'application',
    'RFC': 'keytag',
    'INDOOR': 'in_door',
    '622_IN_FGP': 'fingerprint',
    '622_IN_RFC': 'keytag',
    '622_OUT': 'in_door',
    '622_IN_SVR': 'application',
}
