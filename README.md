# YouTube Repeller


## Preparation

1. Install pi-hole

## How to run

### Clone the repository
```shell
git clone https://github.com/engdan77/mitm_youtube_repeller.git && cd mitm_youtube_repeller
```

### From source
```shell
sudo mitmweb -p 443 --mode regular --set keep_host_header --set validate_inbound_headers=false -s script.py --web-host 0.0.0.0
```

### As docker
```shell
docker build --tag mitm_youtube_repeller . && docker run --name mitm_youtube_repeller -p 443:8080 -d -v $(pwd)/certs:/root/.mitmproxy mitm_youtube_repeller
```