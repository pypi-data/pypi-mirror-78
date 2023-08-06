# Webhook Debugger

## Install
```
curl https://gitlab.com/linalinn/webhook-debugger/raw/master/WebhookDebugger.py -o webhookdebugger.py

```
## Usage

### Exsample 1
1. `$ ./WebhookDebugger.py`
2. `$curl localhost:8080/ -d "some=data"`
#### Exsample Output of WebhookDebugger.py and curl
        WebhookDebugger.py:
        Started http server 0.0.0.0:8811
        SSL disabled
        91.14.105.14 - - [09/Oct/2018 14:00:17] "POST / HTTP/1.1" 200 -
        [POST]:
        /
        [HEADERS]:
        Host: upload-filter.net:8811
        User-Agent: curl/7.60.0
        Accept: */*
        Content-Length: 9
        Content-Type: application/x-www-form-urlencoded
        [BODY]:
        b'some=data'
        [Client IP]:
        127.0.0.1

        curl:
        [POST]:
        /
        [HEADERS]:
        Host: upload-filter.net:8811
        User-Agent: curl/7.60.0
        Accept: */*
        Content-Length: 9
        Content-Type: application/x-www-form-urlencoded
        [BODY]:
        b'some=data'
        [Client IP]:
        XXX.XXX.XXX.XXX

### Exsample 2 with SSl and diffrent response, diffrent Content-Type and diffrent Port
1. `$ ./WebhookDebugger.py -p 8811 -r '{"msg":"JSON says HI"}' -c "application/json" --ssl-cert path/fullchain.pem --ssl-key path/privekey.pem`
2. `$curl exsample.com:8811/ -d "SSL=true"`
#### Exsample Output of WebhookDebugger.py and curl
        WebhookDebugger.py:
        Started http server 0.0.0.0:8811
        SSL enabled
        91.14.105.14 - - [09/Oct/2018 14:22:28] "POST / HTTP/1.1" 200 -
        [POST]:
        /
        [HEADERS]:
        Host: exsample.com:8811
        User-Agent: curl/7.60.0
        Accept: */*
        Content-Length: 8
        Content-Type: application/x-www-form-urlencoded
        [BODY]:
        b'SSL=true'
        [Client IP]:
        XXX.XXX.XXX.XXX

        curl:
        {"msg":"JSON says HI"}
### Forward Option
1. `$ ./WebhookDebugger.py -p 8811 -c "application/json" forward --url exsample.com  --port 443 --use-ssl`
