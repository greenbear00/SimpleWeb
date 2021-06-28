# 구성
1. flask+uwsgi+nginx를 붙임
    - request --[http://localhost:8081]--> nginx --[8081:5000]--> flask+uwsgi [app]
2. logger 수집
    - flask 로그와 nginx 로그를 logstash를 통해서 elastic으로 전송


## logger 셋팅
log 셋팅(nginx와 flask의 log를 logstash를 통하여 elastic으로 전송)
- logger에 대한 logstash pipleline관련하여 grok 문법에 대한 simulate는 kibana에서 [DevTools]->[Grok Debugger]에서 시뮬레이션 할 수 있음
    - logstash grok 문법 참조: https://github.com/logstash-plugins/logstash-patterns-core/blob/v2.0.5/patterns/grok-patterns#L86
- flask에서 내부 logging과 logstash로 log를 전송하게끔 구성함 
    - 실제 flask 내부에서 logstash.TCPLogstashHandler를 통해서 logstash 컨테이너에 log를 전송하게끔 하였음
    - (logstash pipeline관련 내용) .elk/logstash/pipeline/flask_log.conf
    - 로그 예:
        ```
        [flask 로그]
            2021-06-11 01:50:15,033 - web_stream - 192.168.176.1 - GET - OS - requested http://localhost:8080/ - INFO in log - session = no
            2021-06-22 06:34:47,821 - werkzeug - 192.168.240.1 - GET - OS - requested http://localhost:8080/ - INFO in log - session = None


        [logstash 로그]
            {
                "@version" => "1",
                "path" => "log",
                "method" => "GET",
                "loglevel" => "INFO",
                "host" => "flask.simpleweb_elastic",
                "timestamp" => "2021-06-11 01:50:15,018",
                "device" => "OS",
                "requested_url" => "http://localhost:8080/",
                "port" => 56660,
                "message" => "session = no",
                "@timestamp" => 2021-06-11T01:50:15.018Z,
                "clientip" => "192.168.176.1"
            }
        ```
- nginx의 access.log를 logstash로 전송하게끔 구성 (.elk/logstash/pipeline/flask_log.conf)
    - docker-compose 내에서 nginx의 /var/log/nginx 디렉토리에 있는 access.log 를 mount하여 logstash에서 file로 write하게끔 구성 
    - (logstash pipeline관련 내용) .elk/logstash/pipeline/simple_web_log.conf
    - 로그 예:
        ```
        [nginx access.log]
            192.168.176.1 - - [11/Jun/2021:01:50:15 +0000] "GET / HTTP/1.1" 200 280 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36" "-"

        [logstash]
            {
                "tags" => [
                    [0] "_dateparsefailure",
                    [1] "_geoip_lookup_failure"
                ],
                "agents" => {
                    "build" => "",
                    "os" => "Windows",
                    "patch" => "4472",
                    "minor" => "0",
                    "device" => "Other",
                    "os_name" => "Windows",
                    "major" => "91",
                    "name" => "Chrome"
                },
                "agent" => "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
                "@version" => "1",
                "http_version" => "1.1",
                "geoip" => {},
                "path" => "/var/log/nginx/access.log",
                "method" => "GET",
                "bytes" => "280",
                "response" => "200",
                "request" => "/",
                "host" => "b323ff9ed6aa",
                "referrer" => "-",
                "timestamp" => "11/Jun/2021:01:50:15 +0000",
                "message" => "192.168.176.1 - - [11/Jun/2021:01:50:15 +0000] \"GET / HTTP/1.1\" 200 280 \"-\" \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36\" \"-\"",
                "@timestamp" => 2021-06-11T01:50:15.823Z,
                "clientip" => "192.168.176.1"
            }

        ```



- elastic에 /web-YYYY.mm.dd 와 /access-YYYY.mm.dd로 로그가 쌓임
    ```
    [elastic에서 확인 방법]
        GET /web-2021.06.11/_search
        {
            "query": {
                "match_all": {}
            }
        }
    ```

# build
```
./build.sh [start|stop]
```