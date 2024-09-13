# YouTube "shorts" repeller

<img src="https://raw.githubusercontent.com/engdan77/project_images/master/uPic/repeller.png" alt="repeller" style="zoom:33%;" />

## Background and reflections

So this is currently having a 9-year-old kid (together with another one-year-old) who seems to have discovered YouTube and in particular "[YouTube shorts](https://en.wikipedia.org/wiki/YouTube_Shorts)" that appear quite easily to lead to addictive behavior. However, I believe there is some good and educational material on YouTube so I first thought how hard it could be to forbid YouTube shorts, but it turned out to be much more difficult than I first anticipated. There are no good ways to block this feature within the YouTube app or on the web except for disabling history, but someone smart enough would get around that by re-enabling this. So how I instead chose to address this by developing my own MITM-proxy (Man-In-The-Middle proxy) to ensure blocking this certain behavior.

It was not that easy either, but it was possible. So on the device on the network, you would need to ensure allow your self-signed [root certificate](https://en.wikipedia.org/wiki/Root_certificate) allows you to un-encrypt the traffic passing through this solution. But once that obstacle crossed, starting to reverse engineer the traffic passing through I discovered it as I first thought it would be as YouTube appears to have done a terrific job encapsulating all traffic using [Protocol Buffer](https://en.wikipedia.org/wiki/Protocol_Buffers) format that would add another layer of complexity to decoding this, one could think that with help of the URL or path being able to determine "shorts" from "regular videos" but that was not found the case. So essentially I decided to ensure that if videos in general are played more than X number of times within Y minutes I'll ensure to block any more traffic - that way for the kids watching there 5-10 seconds clips rather than a usual clip over several minutes I'll check the originating IP address and add an internal counter. And eventually, block when reaching the threshold. This turns out to work quite well, so I thought I might share this little project in such case other parents may find for this 😄👍



## Simplified visualisation of how this works

<img src="https://raw.githubusercontent.com/engdan77/project_images/master/uPic/mitm_demo.gif" width="200" />




## Preparation

1. Install pi-hole as a local DNS following instructions such as [this](https://pi-hole.net/)

   1. To ensure your DNS will resolve the IP address to the server you run this project at I would modify the `03-pihole-wildcard.conf` to include somethin such as - assuming `10.1.1.1`is the IP address where the above MITM runs:

   ```
   address=/googlevideo.com/10.1.1.1
   ```

2. Follow the MITM proxy installation instructions below

3. Install the certificate you get out from your MITM proxy using instructions like [this](https://docs.mitmproxy.org/stable/concepts-certificates/)

4. Within the `script.py`you can decide if you wish to modify these default settings

   ```
   MAX_VIEWS = 10   # Max video views .. 
   WITHIN_SECONDS = 120  # ... within these number of seconds
   PENALTY_SECONDS = 300   # ... if such happens block for X seconds before able to watch anything more
   ```

   

## Installation of MITM proxy and script for forbidding video streams

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



## Contributions

Always more than welcome, please make Pull Requests or you can always contact me at daniel@engvalls.eu 😇🙏

