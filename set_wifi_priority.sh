#!/bin/bash

# ------------------------------------------------------------------------------
# Script: set_wifi_priority.sh
# Description: This script prioritizes Wi-Fi over Ethernet for internet access
#              by setting a lower route metric for Wi-Fi (wlan0) and a higher
#              metric for Ethernet (eth0) in NetworkManager.
#
# Usage:
# 1. Save the script on your Raspberry Pi:
#    nano set_wifi_priority.sh
#    (Paste the script, then save with CTRL+X, Y, and Enter)
#
# 2. Make the script executable:
#    chmod +x set_wifi_priority.sh
#
# 3. Run the script:
#    ./set_wifi_priority.sh
#
# 4. Verify the routing table (if needed):
#    ip route
#
# Requirements:
# - Raspberry Pi running Raspbian (Raspberry Pi OS) with NetworkManager enabled.
# - A working Wi-Fi and Ethernet connection.
#
# ------------------------------------------------------------------------------

# Check if NetworkManager is running
if ! systemctl is-active --quiet NetworkManager; then
    echo "Error: NetworkManager is not running. Please enable it first."
    exit 1
fi

echo "NetworkManager is active."

# Get the Wi-Fi and Ethernet connection names
WIFI_CONN=$(nmcli -t -f NAME,DEVICE connection show | grep wlan0 | cut -d':' -f1)
ETH_CONN=$(nmcli -t -f NAME,DEVICE connection show | grep eth0 | cut -d':' -f1)

# Check if both connections exist
if [ -z "$WIFI_CONN" ]; then
    echo "Error: No Wi-Fi connection found for wlan0."
    exit 1
fi

if [ -z "$ETH_CONN" ]; then
    echo "Error: No Ethernet connection found for eth0."
    exit 1
fi

echo "Wi-Fi connection detected: $WIFI_CONN"
echo "Ethernet connection detected: $ETH_CONN"

# Set Wi-Fi priority (lower metric) and Ethernet (higher metric)
echo "Setting Wi-Fi ($WIFI_CONN) priority over Ethernet ($ETH_CONN)..."
nmcli connection modify "$WIFI_CONN" ipv4.route-metric 100
nmcli connection modify "$ETH_CONN" ipv4.route-metric 300

# Restart NetworkManager
echo "Restarting NetworkManager..."
sudo systemctl restart NetworkManager

# Verify the settings
echo "Verifying the routing table..."
ip route | grep default

# Confirm persistence after reboot
WIFI_METRIC=$(nmcli connection show "$WIFI_CONN" | grep ipv4.route-metric | awk -F ':' '{print $2}' | xargs)
ETH_METRIC=$(nmcli connection show "$ETH_CONN" | grep ipv4.route-metric | awk -F ':' '{print $2}' | xargs)

if [[ "$WIFI_METRIC" == "100" && "$ETH_METRIC" == "300" ]]; then
    echo "Success: Wi-Fi priority settings are persistent."
else
    echo "Warning: The settings might not persist. Please check manually."
fi

echo "Done!"

