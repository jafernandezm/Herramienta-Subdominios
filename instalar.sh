#!/bin/bash

git clone https://github.com/rbsec/dnscan.git
go install github.com/tomnomnom/httprobe@latest

go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest


