# auto-auto-assistant
## install
```
pip install slack_sdk
```
or use docker:
```
docker build -t python-imagename .
docker run --rm --name CAAAR -e SLACK_WEBHOOK_URL=<SLACK_WEBHOOK_URL> -p 8080 python-imagename
```
## env vars
```
$env:SLACK_BOT_TOKEN = ''
```