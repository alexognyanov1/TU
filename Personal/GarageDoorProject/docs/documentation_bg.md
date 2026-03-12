# Система за дистанционно управление на гаражна врата посредством IoT технологии

**Автор:** Александър Огнянов
**Институция:** Технически университет
**Дата:** Март 2026 г.

---

## Резюме

Настоящата разработка представя проектирането, реализацията и верификацията на система за дистанционно управление на гаражна врата, базирана на интернет на нещата (IoT). Системата интегрира вградено устройство на базата на микроконтролера ESP32, брокер за съобщения по протокол MQTT, Python сървър, изграден с фреймуърка FastAPI, и уеб потребителски интерфейс с удостоверяване чрез JWT. Реализирана е многослойна архитектура, осигуряваща надеждна и сигурна комуникация между компонентите. Системата демонстрира приложимостта на съвременните IoT стандарти за автоматизация на домашни устройства с акцент върху сигурност, надеждност и ниска латентност.

**Ключови думи:** IoT, ESP32, MQTT, FastAPI, JWT, дистанционно управление, вградени системи, домашна автоматизация

---

## 1. Въведение

Домашната автоматизация (Home Automation) е широко изследвана и бързо развиваща се область в контекста на интернет на нещата. Гаражните врати представляват един от най-честите обекти на автоматизация в жилищния сектор, предоставяйки конкретен и измерим случай на употреба (use-case) за IoT система с изисквания за надеждност в реално време.

Основната мотивация на настоящия проект е разработването на система, която:

1. Позволява дистанционно управление на гаражна врата чрез уеб интерфейс от всяко устройство с достъп до интернет.
2. Осигурява сигурност на комуникацията чрез удостоверяване с JSON Web Tokens (JWT) и TLS криптиране на MQTT трафика.
3. Поддържа надеждна асинхронна комуникация с минимална латентност посредством протокола MQTT.
4. Е лесно за разгръщане (deployment) и поддръжка при ограничени хардуерни ресурси.

Настоящата документация описва архитектурата на системата, технологичния стек, детайлната реализация на всеки компонент, схемите на комуникация и съображенията за сигурност.

---

## 2. Системна архитектура

### 2.1 Обзор на архитектурата

Системата е изградена по трислойна архитектура, разграничаваща вградения слой (embedded layer), сървърния слой (backend layer) и презентационния слой (frontend layer). Комуникацията между вградения слой и сървърния слой се осъществява чрез брокера за съобщения Mosquitto по протокола MQTT.

```
┌─────────────────────────────────────────────┐
│           Клиентски слой (Frontend)          │
│     Уеб браузър — статични HTML страници     │
│          GET / и GET /login                  │
└──────────────────┬──────────────────────────┘
                   │ HTTPS / REST API
                   │ (JWT Bearer Token)
┌──────────────────▼──────────────────────────┐
│          Сървърен слой (Backend)             │
│        Python FastAPI + Uvicorn              │
│   /auth/login  /door/trigger  /door/state    │
└──────────────────┬──────────────────────────┘
                   │ MQTT (QoS 1)
                   │ TCP:1883 / WSS:443
┌──────────────────▼──────────────────────────┐
│         Брокер за съобщения                  │
│      Eclipse Mosquitto (Raspberry Pi)        │
│  Listeners: TCP 0.0.0.0:1883, WS 127.0.0.1:9001 │
└──────────────────┬──────────────────────────┘
                   │ MQTT (QoS 1)
                   │ TCP:1883
┌──────────────────▼──────────────────────────┐
│       Вграден слой (Embedded)                │
│           ESP32 — Arduino IDE                │
│    Управление на реле (GPIO relay pin)       │
└──────────────────┬──────────────────────────┘
                   │ GPIO HIGH / LOW
                   ▼
            Мотор на гаражна врата
```

**Фигура 1.** Многослойна архитектура на системата за дистанционно управление на гаражна врата.

### 2.2 Описание на слоевете

| Слой | Технология | Отговорност |
|------|-----------|-------------|
| Клиентски (Frontend) | HTML5, CSS3, Vanilla JavaScript | Потребителски интерфейс, удостоверяване, визуализация на статуса |
| Сървърен (Backend) | Python 3.11, FastAPI, Paho-MQTT | REST API, JWT генерация и верификация, публикуване на MQTT команди |
| Брокер | Eclipse Mosquitto | Маршрутизация на MQTT съобщения между backend и ESP32 |
| Вграден (Embedded) | ESP32, Arduino (C++), PubSubClient, ArduinoJson | Получаване на команди, управление на GPIO реле |

### 2.3 Топик схема на MQTT

| Топик | Публикатор | Примерен payload |
|-------|-----------|-----------------|
| `garage/command` | Backend | `{"action": "trigger"}` |
| `garage/status` | ESP32 | `{"state": "open"}` |

Командният топик (`garage/command`) използва QoS 1 (at-least-once delivery), за да гарантира достигане на командата до ESP32 при временна мрежова прекъсване. Статусният топик (`garage/status`) се публикува с флаг `retained=true`, което позволява на backend да получи последното познато състояние при (пре)свързване.

---

## 3. Хардуерни компоненти

### 3.1 Микроконтролер ESP32

ESP32 е двуядрен микроконтролер (Xtensa LX6, 240 MHz) с вграден WiFi (802.11 b/g/n) и Bluetooth, произведен от Espressif Systems. За целите на настоящия проект са използвани следните ключови характеристики:

- **Безжична свързаност:** WiFi 802.11 b/g/n за свързване към локалната мрежа и MQTT брокера.
- **GPIO:** Изходен GPIO пин, конфигуриран да управлява реле.
- **Watchdog Timer (WDT):** Хардуерен таймер за автоматично рестартиране при зависване.
- **Ниска консумация:** Оптимизирана консумация при активен WiFi режим.

### 3.2 Реле модул

Релейният модул служи като електрически интерфейс между никоволтовата GPIO логика на ESP32 (3.3 V) и управляващата верига на мотора на гаражната врата. При получаване на команда `trigger`, GPIO пинът се активира (HIGH) за конфигурируем период от време (`MOTOR_RUN_DURATION_MS`), след което се деактивира (LOW).

### 3.3 Raspberry Pi (MQTT брокер)

Raspberry Pi е използван като хост за Eclipse Mosquitto MQTT брокера поради ниската му консумация на ток (< 5W) и Linux средата, подходяща за непрекъснато работещи услуги. Брокерът е конфигуриран с два listener-а:

- **Port 1883 (TCP, 0.0.0.0):** За директна комуникация с ESP32 в локалната мрежа.
- **Port 9001 (WebSocket, 127.0.0.1):** За nginx обратен прокси, достъпен само от localhost.

---

## 4. Вграден слой (Embedded)

### 4.1 Технологичен стек

Фърмуерът е реализиран на C++ с използване на Arduino платформата за ESP32. Избраните библиотеки са:

| Библиотека | Версия | Функция |
|-----------|--------|---------|
| PubSubClient (Nick O'Leary) | ≥ 2.8 | MQTT клиент |
| ArduinoJson (Benoit Blanchon) | ≥ 6.x | JSON сериализация / десериализация |
| WiFi (ESP32 Arduino Core) | Вградена | WiFi свързаност |

### 4.2 Конфигурация

Всички чувствителни конфигурационни параметри са изнесени в отделен хедър файл `config.h`, който не се включва в системата за версионен контрол (добавен в `.gitignore`). Предоставен е шаблон `config.h.example`:

```cpp
#define WIFI_SSID             "YOUR_WIFI_SSID"
#define WIFI_PASSWORD         "YOUR_WIFI_PASSWORD"
#define MQTT_BROKER           "192.168.1.100"
#define MQTT_PORT             1883
#define MQTT_USERNAME         "mqtt_user"
#define MQTT_PASSWORD         "mqtt_password"
#define MQTT_CLIENT_ID        "esp32_garage"
#define MQTT_COMMAND_TOPIC    "garage/command"
#define MQTT_STATUS_TOPIC     "garage/status"
#define MOTOR_PIN             4
#define MOTOR_RUN_DURATION_MS 5000
```

### 4.3 Машина на състоянията на вратата

Вратата е моделирана чрез четири дискретни състояния, управлявани от крайна машина на състоянията (Finite State Machine — FSM):

```
STATE_CLOSED ──[trigger]──► STATE_OPENING ──[motor done]──► STATE_OPEN
STATE_OPEN   ──[trigger]──► STATE_CLOSING ──[motor done]──► STATE_CLOSED
```

Всяко ново входящо събитие `trigger`, пристигащо докато моторът работи, се игнорира, с което се предотвратява механично увреждане на задвижващия механизъм.

```cpp
enum DoorState { STATE_CLOSED, STATE_OPENING, STATE_OPEN, STATE_CLOSING };
```

**Таблица 1.** Преходи на машината на състоянията.

| Текущо състояние | Събитие | Следващо състояние |
|-----------------|---------|-------------------|
| STATE_CLOSED | trigger | STATE_OPENING |
| STATE_OPENING | motor done | STATE_OPEN |
| STATE_OPEN | trigger | STATE_CLOSING |
| STATE_CLOSING | motor done | STATE_CLOSED |
| Всяко | trigger (motor running) | (игнорирано) |

### 4.4 Управление на мотора (неблокиращо)

Управлението на мотора е реализирано по неблокиращ начин, базиран на функцията `millis()`, за да не се блокира основният цикъл (`loop()`) и MQTT клиентът да продължи да обработва входящи пакети:

```cpp
void startMotor() {
    digitalWrite(MOTOR_PIN, HIGH);
    motorRunning    = true;
    motorStartedAt  = millis();
}

// Извиква се от loop() при изтичане на таймера
if (motorRunning && millis() - motorStartedAt >= MOTOR_RUN_DURATION_MS) {
    stopMotor();
}
```

### 4.5 WiFi и MQTT свързаност с експоненциален backoff

За надеждна работа при прекъсване на мрежата са реализирани механизми за автоматично преповторно свързване:

- **WiFi:** При загуба на свързаност устройството извиква `connectWiFi()`, която чака до 20 секунди и при неуспех рестартира ESP32 (`ESP.restart()`).
- **MQTT:** Прилага се експоненциален backoff — началното забавяне е 2 s и се удвоява при всеки неуспешен опит до максимум 60 s.

```cpp
reconnectDelay = min(reconnectDelay * 2, (unsigned long)60000);
```

### 4.6 Публикуване на статус с retained флаг

При всяко преминаване в ново състояние ESP32 публикува JSON payload в топика `garage/status` с флаг `retained=true`. Това гарантира, че backend получава последното известно състояние веднага след (пре)свързване, без да е необходимо ново събитие от страна на вратата:

```cpp
mqtt.publish(MQTT_STATUS_TOPIC, payload, /*retained=*/true);
```

---

## 5. Сървърен слой (Backend)

### 5.1 Технологичен стек

| Технология | Версия | Роля |
|-----------|--------|------|
| Python | 3.11+ | Изпълнителна среда |
| FastAPI | 0.135.1 | Уеб фреймуърк (ASGI) |
| Uvicorn | 0.41.0 | ASGI сървър |
| Paho-MQTT | 2.1.0 | MQTT клиент |
| python-jose | 3.5.0 | JWT генерация и верификация |
| pydantic-settings | 2.13.1 | Управление на конфигурация |
| cryptography | 46.0.5 | Криптографски примитиви |

### 5.2 Конфигурация (`config.py`)

Конфигурацията се зарежда от `.env` файл посредством `pydantic-settings`, което осигурява типова безопасност и автоматична валидация:

```python
class Settings(BaseSettings):
    login_username:      str
    login_password:      str
    jwt_secret_key:      str
    mqtt_broker:         str  = "localhost"
    mqtt_port:           int  = 1883
    mqtt_username:       str  = ""
    mqtt_password:       str  = ""
    mqtt_command_topic:  str  = "garage/command"
    mqtt_status_topic:   str  = "garage/status"
    mqtt_transport:      str  = "tcp"
    mqtt_tls:            bool = False

    class Config:
        env_file = ".env"
```

Параметърът `mqtt_transport` приема стойности `"tcp"` (директна локална връзка) или `"websockets"` (при проксиране през nginx с TLS).

### 5.3 Удостоверяване (`auth.py`)

Удостоверяването е реализирано по стандарта OAuth2 с Bearer токени (JWT). Процесът е следният:

1. Клиентът изпраща `POST /auth/login` с JSON тяло `{"username": "...", "password": "..."}`.
2. Backend верифицира идентификационните данни спрямо конфигурираните стойности.
3. При успех се генерира JWT, подписан с алгоритъм HMAC-SHA256 (HS256), с валидност 24 часа.
4. Клиентът съхранява токена в `localStorage` и го изпраща при всяка следваща заявка в хедъра `Authorization: Bearer <token>`.

```python
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 24

def create_access_token(username: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRE_HOURS)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=ALGORITHM)
```

Зависимостта `require_auth` се инжектира в защитените ендпойнти чрез механизма на FastAPI Dependency Injection, което осигурява декларативна и многократно използваема логика за авторизация.

### 5.4 Управление на вратата (`door.py`)

#### 5.4.1 Endpoint `POST /door/trigger`

При получаване на HTTP заявка, ендпойнтът публикува JSON команда в MQTT топика `garage/command`. Блокиращото извикване на Paho-MQTT се изпълнява в отделна нишка (daemon thread) с таймаут от 5 секунди, за да не блокира ASGI event loop-а:

```python
PUBLISH_TIMEOUT_SECONDS = 5

def publish_command(action: str):
    payload = json.dumps({"action": action})
    error: list[Exception] = []

    def _publish():
        try:
            mqtt_publish.single(
                topic=settings.mqtt_command_topic,
                payload=payload,
                hostname=settings.mqtt_broker,
                port=settings.mqtt_port,
                auth=auth,
                transport=settings.mqtt_transport,
                tls=tls,
                qos=1,
            )
        except Exception as e:
            error.append(e)

    thread = threading.Thread(target=_publish, daemon=True)
    thread.start()
    thread.join(timeout=PUBLISH_TIMEOUT_SECONDS)

    if thread.is_alive():
        raise HTTPException(status_code=504, detail="MQTT broker did not respond in time")
    if error:
        raise HTTPException(status_code=502, detail=f"Could not reach MQTT broker: {error[0]}")
```

При недостъпност на брокера системата връща:
- **HTTP 504 Gateway Timeout** — ако брокерът не отговори в рамките на 5 секунди.
- **HTTP 502 Bad Gateway** — при друга мрежова грешка.

### 5.5 Мониторинг на статуса (`state.py`)

#### 5.5.1 MQTT абонамент в background нишка

При стартиране на приложението (lifespan събитие) се инициализира постоянна MQTT клиентска сесия в daemon нишка:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    state.start_state_subscriber()
    yield
```

Абонаментът за топика `garage/status` се регистрира при успешно свързване (`on_connect`). Получените съобщения се разпарсват и in-memory променливата `_door_state` се обновява под защитата на `threading.Lock`:

```python
_door_state: str = "unknown"
_state_lock = threading.Lock()

def _on_message(client, userdata, message):
    payload = json.loads(message.payload)
    state = payload.get("state", "")
    if state in ("open", "opening", "closed", "closing"):
        _set_door_state(state)
```

#### 5.5.2 Endpoint `GET /door/state`

Защитен с `require_auth`, връща последното познато състояние на вратата:

```json
{ "state": "closed" }
```

Валидните стойности са: `"open"`, `"closed"`, `"opening"`, `"closing"`, `"unknown"`.

### 5.6 Маршрутизация на приложението

```python
app.include_router(auth.router)   # /auth/login
app.include_router(door.router)   # /door/trigger, /door/state
app.include_router(state.router)

@app.get("/")      # Сервира index.html
@app.get("/login") # Сервира login.html
```

Статичните HTML файлове се сервират директно от FastAPI посредством `FileResponse`, без нужда от отделен статичен файл сървър.

### 5.7 REST API Документация

#### `POST /auth/login`

| Параметър | Тип | Описание |
|-----------|-----|---------|
| `username` | string (body) | Потребителско име |
| `password` | string (body) | Парола |

**Отговор (200 OK):**
```json
{ "access_token": "<JWT>", "token_type": "bearer" }
```

**Грешки:** 401 Unauthorized при невалидни данни.

---

#### `POST /door/trigger`

**Headers:** `Authorization: Bearer <token>`

**Отговор (200 OK):**
```json
{ "status": "command sent" }
```

**Грешки:** 401 Unauthorized, 502 Bad Gateway, 504 Gateway Timeout.

---

#### `GET /door/state`

**Headers:** `Authorization: Bearer <token>`

**Отговор (200 OK):**
```json
{ "state": "closed" }
```

---

## 6. Презентационен слой (Frontend)

### 6.1 Страница за вход (`login.html`)

Страницата за вход реализира следния процес на удостоверяване:

1. При зареждане проверява дали `localStorage` съдържа валиден токен — при наличие пренасочва директно към `/`.
2. При изпращане на формата изпраща асинхронна `POST` заявка до `/auth/login`.
3. При успех съхранява токена в `localStorage` и пренасочва към контролната страница.
4. При неуспех показва съобщение за грешка.

### 6.2 Контролна страница (`index.html`)

Контролният панел предоставя:

- **Индикатор за статус (state badge):** Показва текущото състояние на вратата с цветово кодиране:
  - Зелено (`state-open`) — отворена
  - Червено (`state-closed`) — затворена
  - Жълто (`state-opening`, `state-closing`) — в движение
  - Сиво (`state-unknown`) — неизвестно

- **Бутон за задействане (Trigger):** Изпраща `POST /door/trigger` при натискане. Бутонът се деактивира временно, за да предотврати двойно изпращане.

- **Автоматично опресняване на статуса:** Polling заявка до `GET /door/state` на всеки 2 секунди.

```javascript
pollState();
setInterval(pollState, 2000);
```

- **Изход (Logout):** Изтрива токена от `localStorage` и пренасочва към `/login`.

### 6.3 Обработка на изтекъл токен

При получаване на HTTP 401 от API, клиентът автоматично изтрива токена и пренасочва към страницата за вход:

```javascript
if (response.status === 401) {
    localStorage.removeItem("token");
    window.location.href = "/login";
    return;
}
```

---

## 7. MQTT Брокер (Mosquitto на Raspberry Pi)

### 7.1 Конфигурация на слушателите

Mosquitto е конфигуриран с два независими listener-а:

```
# /etc/mosquitto/conf.d/garage.conf
listener 1883 0.0.0.0          # Директен TCP за ESP32
listener 9001 127.0.0.1        # WebSocket за nginx proxy (само localhost)
protocol websockets
```

### 7.2 Nginx обратен прокси с TLS

За достъп на backend приложението от интернет, nginx проксира WebSocket трафика към локалния Mosquitto listener с TLS терминация:

```
Internet (WSS:443)  →  nginx (TLS terminate)  →  Mosquitto (WS:9001, localhost)
```

TLS сертификатът се управлява от Let's Encrypt чрез `certbot`.

### 7.3 Конфигурация на backend за продукционна среда

```env
MQTT_BROKER=mqtt.yourdomain.com
MQTT_PORT=443
MQTT_USERNAME=<mqtt_username>
MQTT_PASSWORD=<mqtt_password>
MQTT_TRANSPORT=websockets
MQTT_TLS=true
```

При локална разработка:

```env
MQTT_BROKER=<raspberry-pi-ip>
MQTT_PORT=1883
MQTT_TRANSPORT=tcp
MQTT_TLS=false
```

### 7.4 Firewall конфигурация

Управлението на firewall правилата се осъществява чрез `ufw`:

```bash
sudo ufw allow OpenSSH
sudo ufw allow 1883/tcp comment "MQTT plain TCP"
sudo ufw --force enable
```

Port 9001 (WebSocket) не изисква отваряне в firewall-а, тъй като nginx го достига само на `localhost`.

---

## 8. Сигурност

### 8.1 Удостоверяване и оторизация

Системата реализира следните механизми за сигурност:

| Механизъм | Реализация | Защита срещу |
|-----------|-----------|-------------|
| JWT Bearer токени | python-jose, HS256 | Неоторизиран достъп до API |
| 24-часов TTL на токените | `exp` claim в JWT | Задържани/откраднати токени |
| TLS за MQTT (WSS) | nginx + Let's Encrypt | Прихващане на MQTT трафик |
| Парола за MQTT брокера | mosquitto_passwd | Неоторизирано публикуване |
| `.env` файл (извън VCS) | `.gitignore` | Случайно разкриване на тайни |
| `config.h` извън VCS | `.gitignore` | Компрометиране на устройството |

### 8.2 Управление на тайни (Secrets Management)

Следните файлове са добавени в `.gitignore` и никога не трябва да бъдат включвани в хранилището за код:

```
backend/.env
embedded/GarageDoor/config.h
*.pem
*.key
```

### 8.3 Ограничения на сигурността

- Системата използва единствен потребителски акаунт за web интерфейса, без ролева система (RBAC).
- Паролата се съхранява като plain text в `.env` файл — за продукционна среда се препоръчва хеширане с bcrypt.
- Токените не могат да бъдат явно анулирани (revoked) преди изтичане на TTL, тъй като системата не поддържа token blacklist.

---

## 9. Внедряване (Deployment)

### 9.1 Изисквания

| Компонент | Изисквания |
|-----------|-----------|
| Backend сървър | Python 3.11+, достъп до MQTT брокера |
| MQTT брокер | Raspberry Pi с Mosquitto, портове 1883 и 9001 |
| ESP32 | Arduino IDE, библиотеки PubSubClient и ArduinoJson, WiFi достъп |
| Мрежа | ESP32 и Raspberry Pi в обща LAN, или ESP32 с достъп до публичен IP на брокера |

### 9.2 Разгръщане на backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Попълнете .env с реалните стойности
uvicorn main:app --reload --port 8000
```

### 9.3 Разгръщане на Mosquitto на Raspberry Pi

```bash
# От разработвачката машина
scp mosquitto/deploy.sh pi@<raspberry-pi-ip>:~/deploy.sh
ssh pi@<raspberry-pi-ip> "chmod +x ~/deploy.sh && ~/deploy.sh <mqtt_user> <mqtt_password>"
```

### 9.4 Фърмуер на ESP32

1. Копирайте `config.h.example` → `config.h` и попълнете данните.
2. Инсталирайте PubSubClient и ArduinoJson от Arduino Library Manager.
3. Изберете платка "ESP32 Dev Module".
4. Качете фърмуера (Upload).

### 9.5 Проверка на работоспособността

```bash
# Тест на MQTT брокера (от Raspberry Pi)
mosquitto_sub -h localhost -p 1883 -u <user> -P <pass> -t "garage/command" -v &
mosquitto_pub -h localhost -p 1883 -u <user> -P <pass> -t "garage/command" -m '{"action":"trigger"}'

# Тест на REST API
curl -X POST http://localhost:8000/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"secret"}'
```

---

## 10. Диаграма на потока на данни

### 10.1 Процес на задействане на вратата

```
Потребител                  Frontend              Backend              Mosquitto           ESP32
    │                          │                     │                      │                  │
    │──── натиска Trigger ────►│                     │                      │                  │
    │                          │──POST /door/trigger►│                      │                  │
    │                          │   (Bearer JWT)       │                      │                  │
    │                          │                     │──publish "trigger"──►│                  │
    │                          │                     │  QoS 1               │                  │
    │                          │                     │                      │──on_message()───►│
    │                          │                     │                      │                  │── onTrigger()
    │                          │                     │                      │                  │── GPIO HIGH
    │                          │◄──{ "status": "command sent" }────────────│                  │
    │◄─── "Command sent!" ─────│                     │                      │                  │
    │                          │                     │                      │                  │── (5 секунди)
    │                          │                     │                      │                  │── GPIO LOW
    │                          │                     │                      │◄─ publish status ─│
    │                          │                     │◄───── on_message() ──│                  │
    │                          │──GET /door/state───►│                      │                  │
    │                          │◄──{ "state":"open" }│                      │                  │
    │◄──── badge: "Open" ──────│                     │                      │                  │
```

**Фигура 2.** Последователна диаграма на потока на данни при задействане на вратата.

---

## 11. Ограничения и бъдещи подобрения

### 11.1 Текущи ограничения

1. **Без физически сензори:** Системата не разполага с краен изключвател или магнитен сензор. Промяната на статуса се базира единствено на времето за работа на мотора. При механично препятствие вратата може да спре, докато системата отчита грешно „отворена" позиция.

2. **Единствен потребителски акаунт:** Системата не поддържа множество потребители с различни нива на достъп.

3. **In-memory state:** Статусът на вратата се съхранява в оперативна памет. При рестартиране на backend приложението статусът ще бъде `"unknown"` до следващото съобщение от ESP32.

4. **Без push нотификации:** Клиентът разчита на polling (2 s) вместо на WebSocket/SSE за реално-времево обновяване.

### 11.2 Препоръчани бъдещи подобрения

| Подобрение | Описание | Приоритет |
|-----------|---------|----------|
| Магнитни сензори (reed switch) | Точно определяне на физическата позиция на вратата | Висок |
| WebSocket/SSE за frontend | Елиминиране на polling, реално-времев статус | Среден |
| Многопотребителска система | RBAC с роли admin/viewer | Среден |
| Push нотификации | Сигнализиране при неочаквана промяна на статуса | Среден |
| Персистиране на статуса | SQLite или Redis за съхранение на статуса | Нисък |
| OTA обновяване | Дистанционно обновяване на ESP32 фърмуер | Нисък |

---

## 12. Заключение

Разработената система за дистанционно управление на гаражна врата демонстрира успешна интеграция на съвременни IoT технологии в реален приложен контекст. Архитектурата ефективно разделя отговорностите между трите основни компонента — вграден контролер (ESP32), сървърна логика (FastAPI) и брокер за съобщения (Mosquitto) — като всеки слой е проектиран с оглед на надеждността и сигурността.

Ключовите технически постижения включват:

- Надеждна асинхронна комуникация с QoS 1 гаранции чрез MQTT протокола.
- Неблокиращо управление на мотора на ESP32, позволяващо паралелна обработка на MQTT съобщения.
- Автоматично повторно свързване с експоненциален backoff на всички комуникационни слоеве.
- Многослойна сигурност: JWT удостоверяване на API ниво, TLS криптиране на MQTT трафика, и изолация на тайните от версионния контрол.
- Статусно проследяване чрез retained MQTT съобщения, позволяващо backend да знае последното известно състояние при повторно свързване.

Системата е подходяща основа за разширяване с физически сензори, многопотребителска поддръжка и push нотификации, които да повишат надеждността и потребителското изживяване в производствена среда.

---

## Литература

1. Espressif Systems. (2023). *ESP32 Technical Reference Manual*. Версия 5.1. https://www.espressif.com/sites/default/files/documentation/esp32_technical_reference_manual_en.pdf

2. OASIS Standard. (2019). *MQTT Version 5.0*. OASIS Open. https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html

3. Mosquitto Project. (2024). *Eclipse Mosquitto: An open source MQTT broker*. Eclipse Foundation. https://mosquitto.org/documentation/

4. Ramírez, S. (2024). *FastAPI Documentation*. https://fastapi.tiangolo.com/

5. Jones, M., Bradley, J., & Sakimura, N. (2015). *JSON Web Token (JWT)*. RFC 7519. Internet Engineering Task Force. https://www.rfc-editor.org/rfc/rfc7519

6. O'Leary, N. (2023). *PubSubClient: A client library for the Arduino Ethernet Shield that provides support for MQTT*. https://pubsubclient.knolleary.net/

7. Blanchon, B. (2024). *ArduinoJson: A JSON library for embedded C++*. https://arduinojson.org/

8. van Rossum, G., & others. (2023). *Python 3.11 Documentation*. Python Software Foundation. https://docs.python.org/3.11/

9. Fielding, R. T., & Reschke, J. F. (2014). *Hypertext Transfer Protocol (HTTP/1.1): Authentication*. RFC 7235. IETF. https://www.rfc-editor.org/rfc/rfc7235

10. Rescorla, E. (2018). *The Transport Layer Security (TLS) Protocol Version 1.3*. RFC 8446. IETF. https://www.rfc-editor.org/rfc/rfc8446

---

*Документацията е генерирана на 11 март 2026 г. Всички права запазени.*
