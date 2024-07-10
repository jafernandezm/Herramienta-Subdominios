#!/bin/bash

git clone https://github.com/rbsec/dnscan.git
go install github.com/tomnomnom/httprobe@latest

go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

wget https://github.com/aboul3la/Sublist3r/archive/master.zip .

unzip master.zip



go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest


