#!/bin/bash
# Check the most recent 3 NVIDIA driver releases
python3 ./opensuse_tw_nvidia_validator/nvidia-driver-inspector.py -n 3 --download \
                  --metadata-json $PWD/.workdir/metadata.json
cat ./.workdir/metadata.json