'''
Test Basic WiFi for Pi Pico W

How to create environment file?
https://docs.circuitpython.org/en/latest/docs/environment.html
'''

import os
import ipaddress
import wifi
import socketpool

# Get wifi details from a settings.toml file
print(os.getenv("test_env_file"))
ssid = os.getenv("WIFI_SSID")
password = os.getenv("WIFI_PASSWORD")

print("Connecting to WiFi '{}' ... ".format(ssid), end="")

#  Connect to Wi-Fi AP
wifi.radio.connect(ssid, password)

print("connected!")
print()

pool = socketpool.SocketPool(wifi.radio)

#  Print MAC address
print("Pico W MAC address: ", [hex(i) for i in wifi.radio.mac_address])

#  Print IP address
print("Pico W IP address: ", wifi.radio.ipv4_address)
print()

#  Ping to google.com
ipv4 = ipaddress.ip_address("8.8.4.4")
print("Ping to google.com: %f ms" % (wifi.radio.ping(ipv4)*1000))
