# **🏠 Home Assistant Zigbang Doorlock Integration**

이 통합 구성요소(Custom Component)는 **직방(구 삼성 SDS) 스마트 도어락**을 Home Assistant와 연동하여 상태 모니터링, 배터리 관리, 원격 제어를 가능하게 합니다. 공식 앱의 기능을 HA 내에서 자동화 및 대시보드로 확장할 수 있습니다.

---

### **✨ 주요 기능**

*   **실시간 상태 동기화**: 도어락의 잠금/해제 상태를 실시간으로 모니터링하며 HA의 `lock` 엔티티와 동기화합니다.
*   **재택 안심 모드 스위치**: 직방 앱의 재택 안심 모드를 Home Assistant 내에서 켜고 끌 수 있는 `switch` 엔티티를 제공합니다.
*   **원격 보안 제어**: HA 대시보드 및 서비스 호출을 통해 안전하게 문을 열 수(Unlock) 있습니다.
*   **지능형 배터리 관리**: 배터리 잔량을 별도의 센서(`sensor`) 엔티티로 제공하여 교체 시기를 푸시 알림으로 설정할 수 있습니다.
*   **정밀한 출입 이력 분석**: 지문, 카드, 앱, 내부 수동 개폐 등 출입 수단과 사용자 정보를 엔티티의 속성(Attributes) 데이터로 상세히 제공합니다.
*   **즉각적인 알림(Event) 트리거**: 전용 `event` 플랫폼 지원으로 도어락 출입 알림을 자동화에 손쉽게 연동할 수 있습니다.
*   **자동 세션 복구**: API 인증 만료 시 자동으로 재로그인을 수행하여 끊김 없는 연결성을 유지합니다.
*   **타임존 자동 보정**: 서버의 UTC 시간을 한국 표준시(KST) 및 사용자의 지역 시간대에 맞춰 자동으로 변환합니다.

---

### **📂 디렉토리 구조**

```text
ha-zigbang-doorlock/
├── custom_components/
│   └── zigbang_doorlock/
│       ├── __init__.py      # 데이터 업데이트 코디네이터 및 통합 구성요소 초기화
│       ├── api.py           # 직방 클라우드 서버와의 REST API 통신 로직
│       ├── const.py         # 도메인, 기본 설정값 등 상수 정의
│       ├── event.py         # 출입 이력 및 실시간 알림 이벤트 엔티티 구현
│       ├── lock.py          # 도어락 잠금/해제 기능 엔티티 구현
│       ├── sensor.py        # 배터리 잔량 및 상태 센서 엔티티 구현
│       ├── util.py          # 타임존 변환 및 랜덤 IMEI 생성 등 유틸리티
│       ├── manifest.json    # 통합 구성요소 메타데이터 및 의존성 정의
│       ├── brand/           # Home Assistant UI에 표시될 로고 및 아이콘
│       └── translations/    # 다국어 지원 (UI 번역) 파일
└── tests/                   # 개발용 단위/통합 테스트 코드
```

---

### **� 엔티티 속성 (Attributes) 및 가능한 값**

`lock` 및 `event` 엔티티는 자동화 스크립트에서 다양하게 활용할 수 있도록 출입 상태 정보를 세분화하여 속성(Attribute)으로 제공합니다.

#### **1. Lock 엔티티 (`lock.*_lock`)**
가장 최근의 출입 이력 정보를 저장합니다.

| 속성명 | 설명 | 가능한 값 (Possible Values) |
| :--- | :--- | :--- |
| `last_event_at` | 마지막 이벤트 발생 시간 | ISO 8601 시간 (예: `2024-05-18T14:30:00+09:00`) |
| `last_message` | 직방 API 알림 메시지 원문 | 문자열 (예: `홍길동님이 지문으로 문을 열었습니다.`) |
| `last_alert_type` | 도어락 상태 및 이벤트 유형 | `locked`, `unlocked`, `unlock_failed_5_times`, `unlocked_for_30_seconds`, `lock_failed` |
| `last_unlock_tool` | 잠금 해제 인증 수단 | `fingerprint`(지문), `application`(앱), `keytag`(카드), `voice`(음성), `face`(얼굴인식), `number`(키패드입력), `in_door_button`(내부 수동), `null`(없음) |
| `last_user_name` | 인증된 사용자의 이름 | 사용자 이름 (예: `홍길동`) 또는 `null` |
| `event_id` | 직방 시스템의 이벤트 고유 식별자 | 숫자/문자열 ID (예: `12345678`) |

#### **2. Event 엔티티 (`event.*_event`)**
새로운 이벤트 발생 시 이벤트 버스를 통해 전달되는 데이터 및 엔티티 속성입니다.

| 속성명 | 설명 | 가능한 값 (Possible Values) |
| :--- | :--- | :--- |
| `event_type` | HA 이벤트 플랫폼 종류 | `doorlock_alert` (고정값) |
| `message` | 직방 API 알림 메시지 원문 | 문자열 |
| `alert_type` | 도어락 상태 및 이벤트 유형 | `locked`, `unlocked`, `unlock_failed_5_times`, `unlocked_for_30_seconds`, `lock_failed` |
| `unlock_tool` | 잠금 해제 인증 수단 | `fingerprint`, `application`, `keytag`, `in_door`, `null` |
| `user_name` | 인증된 사용자의 이름 | 사용자 이름 또는 `null` |
| `alert_at` | 이벤트 발생 시간 | ISO 8601 시간 (예: `2024-05-18T14:30:00+09:00`) |

💡 **Tip**: 자동화 작성 시 `alert_type`이 `unlock_failed_5_times`이거나 `lock_failed`인 경우 보안 경고 알림(Siren 등)을 울리도록 구성할 수 있습니다.

---

### **🔧 설치 및 설정**

#### **1. HACS 설치 (권장)**
1. Home Assistant 사이드바에서 **HACS**로 이동합니다.
2. 우측 상단 **⋮** 메뉴에서 **사용자 정의 저장소(Custom repositories)**를 선택합니다.
3. 저장소 URL에 아래 주소를 입력합니다.
   ```text
   https://github.com/heygoodluck/ha-zigbang-doorlock
   ```
4. Category는 **Integration**으로 선택한 뒤 **Add**를 누릅니다.
5. HACS에서 **Zigbang Doorlock** 또는 **직방 도어락**을 검색해 설치합니다.
6. Home Assistant를 **재시작**합니다.

#### **2. 수동 설치**
1. Home Assistant의 설정 디렉토리(`config/`) 내부의 `custom_components/` 폴더로 이동합니다. (폴더가 없으면 생성하세요.)
2. Repo 내 `custom_components/zigbang_doorlock/` 폴더를 Home Assistant의 `custom_components/zigbang_doorlock/` 경로로 복사합니다.
3. Home Assistant를 **재시작**합니다.

#### **3. Home Assistant 설정**
아래 3-1 UI 설정 혹은 3-2 YAML 파일 설정 중 하나를 수행합니다.

##### **3-1. 통합 구성요소 추가 (UI 설정)**
1. Home Assistant 사이드바에서 **설정(Settings)** > **기기 및 서비스(Devices & Services)**로 이동합니다.
2. 우측 하단의 **통합 구성요소 추가(Add Integration)** 버튼을 클릭합니다.
3. **Zigbang Doorlock**을 검색하여 선택합니다.
4. 직방 계정 정보(아이디, 비밀번호)와 IMEI(선택 사항)를 입력하고 확인을 누릅니다.

##### **3-2. YAML 설정 (Configuration 수동 설정)**
`configuration.yaml` 파일에 아래 내용을 추가하고 사용자 정보를 입력합니다.
```yaml
# zigbang_doorlock 설정 예시
zigbang_doorlock:
  username: "YOUR_ZIGBANG_ID"        # 직방 앱 로그인 이메일 계정
  password: "YOUR_ZIGBANG_PASSWORD"  # 직방 앱 비밀번호
  imei: "YOUR_DEVICE_IMEI"           # (선택 사항) 스마트폰의 IMEI 값
```

---

### **💡 IMEI 설정 가이드**

직방 API 보안 정책상 **동일 계정에서 새로운 IMEI로 로그인할 경우 기존 기기는 로그아웃** 처리됩니다.

*   **공존 모드 (추천)**: 현재 사용 중인 스마트폰 앱의 IMEI 값을 확인하여 입력하세요. 앱과 HA가 동일한 기기로 인식되어 양쪽 모두 로그인이 유지됩니다.
*   **독립 모드**: 별도의 계정을 사용하거나 앱 로그아웃이 상관없다면 `imei` 항목을 비워두세요. 시스템이 자동으로 고유한 무작위 값을 생성합니다.

---

### **🤖 자동화 활용 예시**

> ⚠️ **주의 (알림 누락 방지)**: `lock` 엔티티의 속성 변화(`platform: state`)를 트리거로 사용할 경우, 10초 간격의 상태 조회(Polling) 특성상 짧은 시간 안에 여러 번의 출입이 발생하면 최신 데이터로 덮어씌워져 **일부 알림 누락**이 발생할 수 있습니다. 누락 없는 안정적인 알림을 위해서는 아래의 **Event 방식(권장)**을 사용하시기 바랍니다.

#### **1. Event 방식을 활용한 알림 (권장)**
Home Assistant의 이벤트 버스를 직접 수신하여, 10초 주기 내에 연속으로 발생한 이벤트도 모두 누락 없이 처리합니다.

```yaml
alias: "[보안] 현관문 실시간 출입 알림 (Event 방식)"
description: "이벤트 버스를 활용하여 누락 없이 알림을 발송합니다."
trigger:
  - platform: event
    event_type: zigbang_doorlock_alert
action:
  - variables:
      user_name: "{{ trigger.event.data.user_name }}"
      msg_text: "{{ trigger.event.data.message }}"
      friendly_msg: >-
        {% if user_name %}
          {{ user_name }}님이 인증을 통해 입실하였습니다.
        {% else %}
          {{ msg_text }}
        {% endif %}
    service: notify.mobile_app_your_smartphone
    data:
      title: "🏠 도어락 알림"
      message: "{{ friendly_msg }}"
      data:
        group: "doorlock-events"
        clickAction: "/lovelace/security"
```

#### **2. Lock 엔티티 속성을 활용한 알림 (참고용)**
기존처럼 `lock` 엔티티의 `event_id` 속성 변화를 감지하여 스마트폰으로 푸시 알림을 보내는 자동화 스크립트입니다.

```yaml
alias: "[보안] 현관문 실시간 출입 알림"
description: "엔티티 속성을 활용하여 알림을 발송합니다."
trigger:
  - platform: state
    entity_id: lock.zigbang_doorlock
    attribute: event_id  # 새로운 출입 이벤트 발생 시 트리거
action:
  - variables:
      user_name: "{{ state_attr(trigger.entity_id, 'last_user_name') }}"
      msg_text: "{{ state_attr(trigger.entity_id, 'last_message') }}"
      friendly_msg: >-
        {% if user_name %}
          {{ user_name }}님이 인증을 통해 입실하였습니다.
        {% else %}
          {{ msg_text }}
        {% endif %}
    service: notify.mobile_app_your_smartphone
    data:
      title: "🏠 도어락 알림"
      message: "{{ friendly_msg }}"
      data:
        group: "doorlock-events"
        clickAction: "/lovelace/security"
```

---

### **⚖️ 면책 조항 (Disclaimer)**

*   본 프로젝트는 개인이 직방 API를 분석하여 제작한 **비공식(Unofficial)** 통합 구성요소입니다.
*   직방(Zigbang) 측의 API 사정이나 정책 변경에 따라 기능이 제한되거나 중단될 수 있습니다.
*   과도한 API 요청(Polling)은 계정 일시 차단의 원인이 될 수 있으므로 주의하십시오.
*   본 소프트웨어 사용으로 인해 발생하는 기기 오작동, 보안 사고 등 어떠한 결과에 대해서도 개발자는 책임을 지지 않습니다.
