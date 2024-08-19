# YouTube Repeller


## Preparation

1. Install pi-hole

## How to run

### From source
```shell
sudo mitmweb -p 443 --mode regular --set keep_host_header --set validate_inbound_headers=false -s mitm_youtube_repeller.py --web-host 0.0.0.0
```

### As docker
```shell
docker run --name mitm_youtube_repeller --rm -d -p 443:8080 -v $(pwd):/data  mitmproxy/mitmproxy mitmproxy -s /data/scripts/redirect.py -s /data/mitm_youtube_repeller.py
docker logs mitmproxy -f
```