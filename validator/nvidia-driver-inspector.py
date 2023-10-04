"""
Inspect the most recent 5 releases of NVIDIA driver on AMD64 arch.
Provide options to download and unpack them to a specified directory.
"""
import argparse
from dataclasses import dataclass
from typing import Optional

# NVIDIA driver link URL
# https://us.download.nvidia.com/XFree86/Linux-x86_64/535.113.01/NVIDIA-Linux-x86_64-535.113.01.run
NVIDIA_DRIVER_URL = "https://us.download.nvidia.com/XFree86/Linux-x86_64/{version}/NVIDIA-Linux-x86_64-{version}.run"
NVIDIA_DRIVER_ARCHIVE = "https://www.nvidia.com/en-us/drivers/unix/linux-amd64-display-archive/"

@dataclass
class NVIDIADriverMetadata:
    version: str
    release_date: str
    build_status: bool
    build_error: Optional[str]=None

def fetch_nvidia_driver_metadata(n: int=5):
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int, default=5, help="Inspect and fetch the most recent N nvidia driver releases.")
    parser.add_argument("-o", type=str, help="Download the drivers to the given directory.")
    parser.add_argument("--build", type=str, help="try building the given directory, and store the results in output.")
    args = parser.parse_args()
    metadata = fetch_nvidia_driver_metadata(args.n)
