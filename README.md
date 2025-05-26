# auto-auto-assistant
## Slack
### install
```
pip install slack_sdk
```
or use docker:
```
docker run --rm --name CAAAR -e SLACK_WEBHOOK_URL=<SLACK_WEBHOOK_URL> ghcr.io/rubenteck/caaar
```
build with docker:
```
docker build -t caaar .
docker run --rm --name CAAAR -e SLACK_WEBHOOK_URL=<SLACK_WEBHOOK_URL> caaar
```
### env vars
```
$env:SLACK_BOT_TOKEN = ''
```
## HASS
This is WIP and doesn't work yet! don't use this!
### install
install the local addon in your HASS (after downloading it). run the following command if you do not already have a HASS instance:
```
docker run -d \
  --name homeassistant \
  --privileged \
  --restart=unless-stopped \
  -e TZ=MY_TIME_ZONE \
  -v /PATH_TO_YOUR_CONFIG:/config \
  -v /run/dbus:/run/dbus:ro \
  --network=host \
  ghcr.io/home-assistant/home-assistant:stable
```

docker run -d --name homeassistant --privileged --restart=unless-stopped -p 8123 -e TZ=BE -v ./config:/config -v /run/dbus:/run/dbus:ro --network=host ghcr.io/home-assistant/home-assistant:stable

