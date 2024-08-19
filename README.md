# YouTube Repeller


## Preparation

1. Install pi-hole

## How to run

### From source
```shell
sudo mitmweb -p 443 --mode regular --set keep_host_header --set validate_inbound_headers=false -s mitm_youtube_repeller.py --web-host 0.0.0.0
```