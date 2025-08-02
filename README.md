# TeleGlow
Telegram bot to let you control user Wiz light

# Configuration
1. Create a new bot from Telegram Bot Father
2. Edit config.yml
```
telegram:
  webhook_url: "https://your-webhook-url-for-telegram-call.com"
  token: "0000000000:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
  port: 5566

bulb:
  init_mode: "discovery" # Options: "static", "discovery"
  wiz_bulb_ip: # Required if init_mode is "static"
    - name: "Bulb1"
      ip: "192.168.1.101"
    - name: "Bulb2"
      ip: "192.168.1.102"
    - name: "Bulb3"
      ip: "192.168.1.103"
    - name: "Bulb4"
      ip: "192.168.1.104"
  discovery_broadcast_ip: "192.168.1.255" # Required if init_mode is "discovery"

# telegram user id - only these users can control bulb
users:
  - 000000000
```
3. Install necessary dependency and run container
```
docker run -p <PORT>:<PORT> -v <PATH_OF_config.yml>:/app/config.yml <IMAGE>
```
