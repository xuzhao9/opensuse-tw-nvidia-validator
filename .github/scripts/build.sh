#!/bin/bash
# Try building NVIDIA driver releases
mkdir -p /workspace/.workdir/build
python3 ./opensuse_tw_nvidia_validator/nvidia-driver-inspector.py \
                  --metadata-json $PWD/.workdir/metadata.json \
                  --output-json $PWD/.workdir/build/build.json
cat /workspace/.workdir/build/build.json