#!/bin/bash

# Install python deps
zypper in -y python3 python311-beautifulsoup4 python311-requests \
	python311-urllib3 python311-distro

# Install kernel deps
zypper in -y make gcc kernel-default-devel kernel-devel git vim
