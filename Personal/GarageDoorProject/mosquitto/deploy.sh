#!/usr/bin/env bash
# deploy.sh — Installs and configures Mosquitto on a Raspberry Pi.
#
# Usage:
#   chmod +x deploy.sh
#   ./deploy.sh <mqtt_username> <mqtt_password>
#
# Run this on the Raspberry Pi (not your development machine).

set -euo pipefail

MQTT_USER="${1:-}"
MQTT_PASS="${2:-}"

if [[ -z "$MQTT_USER" || -z "$MQTT_PASS" ]]; then
  echo "Usage: $0 <mqtt_username> <mqtt_password>"
  exit 1
fi

# ── 1. Install Mosquitto ──────────────────────────────────────────────────────

echo ">>> Updating package list..."
sudo apt-get update -q

echo ">>> Installing Mosquitto..."
sudo apt-get install -y mosquitto mosquitto-clients

# ── 2. Create the password file ───────────────────────────────────────────────

echo ">>> Creating MQTT user: $MQTT_USER"
sudo mosquitto_passwd -c /etc/mosquitto/passwd "$MQTT_USER" <<< "$MQTT_PASS
$MQTT_PASS"

# ── 3. Write the configuration file ──────────────────────────────────────────

echo ">>> Removing duplicate auth directives from main mosquitto.conf..."
sudo sed -i '/^allow_anonymous/d' /etc/mosquitto/mosquitto.conf
sudo sed -i '/^password_file/d' /etc/mosquitto/mosquitto.conf

echo ">>> Writing /etc/mosquitto/conf.d/garage.conf"
sudo tee /etc/mosquitto/conf.d/garage.conf > /dev/null << 'EOF'
# Auth applies globally to all listeners below.
allow_anonymous false
password_file /etc/mosquitto/passwd

# Plain TCP — for the ESP32 (direct connection, no nginx).
# 0.0.0.0 is required in Mosquitto 2.0+ to accept non-localhost connections.
listener 1883 0.0.0.0

# WebSocket — for the Python backend connecting through nginx.
# Localhost only; nginx is the sole external entry point for this port.
listener 9001 127.0.0.1
protocol websockets

# Log to syslog (view with: sudo journalctl -u mosquitto -f)
log_dest syslog
log_type error
log_type warning
log_type notice
EOF


# ── 5. Enable and (re)start the service ──────────────────────────────────────

echo ">>> Enabling and starting Mosquitto..."
sudo systemctl enable mosquitto
sudo systemctl restart mosquitto

# ── 5. Verify ─────────────────────────────────────────────────────────────────

echo ""
echo ">>> Mosquitto status:"
sudo systemctl is-active mosquitto && echo "Mosquitto is running." || echo "WARNING: Mosquitto failed to start."

echo ""
echo ">>> Quick connectivity test (subscribe + publish):"
mosquitto_sub -h localhost -u "$MQTT_USER" -P "$MQTT_PASS" -t "test/ping" -C 1 &
SUB_PID=$!
sleep 0.5
mosquitto_pub -h localhost -u "$MQTT_USER" -P "$MQTT_PASS" -t "test/ping" -m "pong"
wait $SUB_PID && echo "Test passed — broker is accepting authenticated connections."

echo ""
echo "Done. Mosquitto is installed and running."
echo "Update backend/.env with:"
echo "  MQTT_BROKER=<raspberry-pi-ip>"
echo "  MQTT_USERNAME=$MQTT_USER"
echo "  MQTT_PASSWORD=<the password you provided>"
