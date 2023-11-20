#!/bin/bash

# Install python deps
sudo zypper in -y python3 python311-beautifulsoup4 python311-requests python311-urllib3

# Install kernel deps
sudo zypper in -y make gcc kernel-default-devel kernel-devel git
