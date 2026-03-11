# Mosquitto Setup on Raspberry Pi

Mosquitto is the MQTT broker that sits between the Python backend and the ESP32. It runs on the Raspberry Pi and must be reachable by both.

## How clients connect

| Client         | Protocol         | Path                                      |
|----------------|------------------|-------------------------------------------|
| ESP32          | Plain MQTT (TCP) | Directly on port 1883                     |
| Python backend | MQTT over WSS    | `wss://mqtt.yourdomain.com` via nginx     |

Mosquitto runs two listeners:
- **Port 1883** (`0.0.0.0`) — plain TCP for the ESP32
- **Port 9001** (`127.0.0.1`) — WebSocket for nginx to proxy, localhost only

## Prerequisites

- Raspberry Pi running Raspberry Pi OS (Bookworm / Bullseye)
- SSH access to the Pi
- nginx already running on the Pi with ports 80 and 443 set up
- Port **1883** forwarded on your router (for the ESP32 direct connection)
- A subdomain pointed at the Pi's public IP (e.g. `mqtt.yourdomain.com`) for the backend connection

## Quick deploy

Copy the script to the Pi and run it:

```bash
# From your development machine
scp mosquitto/deploy.sh pi@<raspberry-pi-ip>:~/deploy.sh
ssh pi@<raspberry-pi-ip> "chmod +x ~/deploy.sh && ~/deploy.sh <mqtt_username> <mqtt_password>"
```

The script will:
1. Install `mosquitto` and `mosquitto-clients`
2. Create an authenticated MQTT user
3. Write a config with a plain TCP listener (`0.0.0.0:1883`) and a WebSocket listener (`127.0.0.1:9001`)
4. Open port 1883 in `ufw` (enabling it first if needed, keeping SSH open)
5. Enable Mosquitto as a systemd service
6. Run a quick publish/subscribe test to confirm everything works

## Setting up the nginx site

Copy the nginx config to the Pi and enable it:

```bash
# From your development machine
scp mosquitto/nginx-mqtt.conf pi@<raspberry-pi-ip>:~/nginx-mqtt.conf
ssh pi@<raspberry-pi-ip>
```

On the Pi:
```bash
# Edit the file to replace "mqtt.yourdomain.com" with your actual subdomain
nano ~/nginx-mqtt.conf

# Install the site
sudo cp ~/nginx-mqtt.conf /etc/nginx/sites-available/mqtt
sudo ln -s /etc/nginx/sites-available/mqtt /etc/nginx/sites-enabled/mqtt

# Obtain a TLS certificate for the subdomain
sudo certbot --nginx -d mqtt.yourdomain.com

# Test and reload nginx
sudo nginx -t && sudo systemctl reload nginx
```

## Updating the backend `.env`

Once the domain is live, update `backend/.env` to connect via WebSocket Secure through nginx:

```env
MQTT_BROKER=mqtt.yourdomain.com
MQTT_PORT=443
MQTT_USERNAME=<mqtt_username>
MQTT_PASSWORD=<mqtt_password>
MQTT_TRANSPORT=websockets
MQTT_TLS=true
```

`MQTT_TLS=true` is required because nginx serves port 443 with TLS (WSS, not plain WS).
Without it paho will attempt a plain WebSocket handshake into a TLS socket and fail
with a protocol error.

For local development without a domain, keep the direct TCP connection:

```env
MQTT_BROKER=<raspberry-pi-ip>
MQTT_PORT=1883
MQTT_USERNAME=<mqtt_username>
MQTT_PASSWORD=<mqtt_password>
MQTT_TRANSPORT=tcp
MQTT_TLS=false
```

## Useful commands on the Pi

```bash
# Check service status
sudo systemctl status mosquitto

# Watch live logs
sudo journalctl -u mosquitto -f

# Restart after a config change
sudo systemctl restart mosquitto

# Test plain TCP on port 1883 (on the Pi, or from the local network)
mosquitto_sub -h localhost -p 1883 -u <user> -P <pass> -t "garage/command" -v
mosquitto_pub -h localhost -p 1883 -u <user> -P <pass> -t "garage/command" -m '{"action":"trigger"}'

# Test via the domain using WebSocket Secure (WSS) — port 443 through nginx.
# The -L flag takes a full URL; the path /mqtt is where Mosquitto's WebSocket
# listener expects connections.
# Note: plain "-h mqtt.yourdomain.com -p 443" will fail with a protocol error
# because nginx speaks TLS on 443, not plain MQTT.
mosquitto_sub -L "wss://mqtt.amai.bg/mqtt" -u <user> -P <pass> -t "garage/command" -v
mosquitto_pub -L "wss://mqtt.amai.bg/mqtt" -u <user> -P <pass> -t "garage/command" -m '{"action":"trigger"}'

# Add an additional MQTT user
sudo mosquitto_passwd /etc/mosquitto/passwd <new_username>
sudo systemctl restart mosquitto
```

## Configuration file

The deploy script writes `/etc/mosquitto/conf.d/garage.conf`. To edit it manually:

```bash
sudo nano /etc/mosquitto/conf.d/garage.conf
sudo systemctl restart mosquitto
```

## Firewall

The deploy script handles this automatically. To redo manually:

```bash
sudo ufw allow OpenSSH          # keep SSH open before enabling ufw
sudo ufw --force enable
sudo ufw allow 1883/tcp comment "MQTT plain TCP"
sudo ufw reload
sudo ufw status
```

Port 9001 (WebSocket) does **not** need to be opened in the firewall — nginx reaches it on localhost.

## Router / NAT

Forward **TCP port 1883** to the Pi's local IP for the ESP32. The WebSocket path (`wss://mqtt.yourdomain.com`) uses port 443, which you have already forwarded via your existing nginx setup.
