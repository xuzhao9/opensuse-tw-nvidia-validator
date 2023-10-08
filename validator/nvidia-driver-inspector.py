"""
Inspect the most recent 5 releases of NVIDIA driver on AMD64 arch.
Provide options to download and unpack them to a specified directory.
"""
import argparse
from bs4 import BeautifulSoup
import dataclasses
from dataclasses import dataclass
from datetime import datetime
import json
import os
import re
import requests
import subprocess
import urllib
from typing import Optional, Any, List

# NVIDIA driver link URL
# https://us.download.nvidia.com/XFree86/Linux-x86_64/535.113.01/NVIDIA-Linux-x86_64-535.113.01.run
NVIDIA_DRIVER_URL = "https://us.download.nvidia.com/XFree86/Linux-x86_64/{version}/NVIDIA-Linux-x86_64-{version}.run"
NVIDIA_DRIVER_ARCHIVE = "https://www.nvidia.com/en-us/drivers/unix/linux-amd64-display-archive/"
DEFAULT_TEST_VERSIONS = 3

@dataclass
class NVIDIADriverMetadata:
    version: str
    release_date: datetime

@dataclass
class NVIDIADriverBuildResult:
    metadata: NVIDIADriverMetadata
    opensuse_snapshot_version: str
    kernel_version: str
    build_success: bool

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        elif isinstance(o, datetime):
            return datetime.strftime(o, '%Y%m%d')
        return super().default(o)

def _get_filename_from_url(url: str) -> str:
    return url.rsplit('/', 1)[-1]

def download_url(url: str, tp: str="text", filename: str=None) -> Any:
    "Download webpage or file from url to a path"
    if tp == "text":
        response = requests.get(url)
        return response.text
    elif tp == "binary":
        assert filename, "Must specify file name when downloading a binary."
        urllib.request.urlretrieve(url, filename)

def download_driver(version: str, target_dir: str):
    driver_full_url = NVIDIA_DRIVER_URL.format(version=version)
    driver_file_name = _get_filename_from_url(driver_full_url)
    version_dir = os.path.join(target_dir, version)
    os.makedirs(version_dir, exist_ok=True)
    target_full_path = os.path.join(target_dir, version, driver_file_name)
    if os.path.exists(target_full_path):
        return
    print(f"Downloading nvidia driver {version}...", end="", flush=True)
    download_url(driver_full_url, tp="binary", filename=target_full_path)
    print("[Done]", flush=True)

def _get_version_from_p(p: str):
    regex = 'Version: ([0-9\.]+)'
    version = re.search(regex, p).groups()[0]
    return version

def _get_release_date_from_p(p: str):
    regex = 'Release Date:(.*, [0-9]+)'
    release_date = re.search(regex, p).groups()[0].strip()
    # Replace typos
    release_date = release_date.replace("Jaunary", "January")
    release_date = release_date.replace("Auguts", "August")
    try:
        date = datetime.strptime(release_date, '%B %d, %Y')
    except ValueError:
        date = datetime.strptime(release_date, '%b %d, %Y')
    return date

def _get_most_recent_versions(metadata: List[NVIDIADriverMetadata], n: int) -> List[NVIDIADriverMetadata]:
    if len(metadata) < n:
        return metadata
    sorted(metadata, key=lambda x: x.release_date, reverse=True)
    return metadata[:n]

def fetch_nvidia_driver_metadata(n: int=DEFAULT_TEST_VERSIONS) -> List[NVIDIADriverMetadata]:
    url_text = download_url(NVIDIA_DRIVER_ARCHIVE, "text")
    # Parse the text
    soup = BeautifulSoup(url_text, 'html.parser')
    versions = []
    td_elements = soup.find_all('div', {"class", "pressItem"})
    for e in td_elements:
        versions.extend(e.find_all('p')) 
    versions = list(map(lambda x: x.text, versions))
    versions = list(filter(lambda x: "Version" in x, versions))
    metadata = list(map(lambda x: NVIDIADriverMetadata(
        version=_get_version_from_p(x),
        release_date=_get_release_date_from_p(x),
    ), versions))
    return _get_most_recent_versions(metadata, n)

def _get_driver_file_name(base_dir: str, version: str) -> str:
    driver_file_dir = os.path.join(base_dir, version)
    run_files = list(filter(lambda x: x.endswith(".run") and x.startswith("NVIDIA"), os.listdir(driver_file_dir)))
    assert len(run_files), f"Couldn't find expected NVIDIA driver file at {driver_file_dir}!"
    return run_files[0]

# extract the driver and return the extracted directory path
def preprocess_driver_file(driver_file_name: str, driver_file_path: str) -> str:
    pass

def try_build_driver(metadata: NVIDIADriverMetadata, driver_directory_path: str) -> NVIDIADriverBuildResult:
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int, default=DEFAULT_TEST_VERSIONS, help="Inspect and fetch the most recent N nvidia driver releases.")
    parser.add_argument("--download", action="store_true", help="Download the drivers to the given directory.")
    parser.add_argument("--build", action="store_true", help="Try building the given directory, and store the results in output.")
    parser.add_argument("--metadata-json", type=str, help="Specify the metadata json file.")
    parser.add_argument("--build-json", type=str, help="Specify the build result json file.")
    args = parser.parse_args()
    if args.metadata_json:
        metadata = fetch_nvidia_driver_metadata(args.n)
        print(metadata)
        with open(args.metadata_json, "w") as mj:
            mj.write(json.dumps(metadata, cls=EnhancedJSONEncoder, indent=4))
        metadata_dir = os.path.dirname(args.metadata_json)
        if args.download:
            for m in metadata:
                download_driver(m.version, target_dir=metadata_dir)
    elif args.build_json:
        with open(args.metadata_json, "r") as mj:
            metadata = json.loads(mj, cls=EnhancedJSONEncoder)
        metadata_dir = os.path.dirname(args.metadata_json)
        build_result_dir = os.path.dirname(args.build_json)
        build_results = []
        for m in metadata:
            driver_file_name = _get_driver_file_name(metadata_dir, m.version)
            driver_dir = preprocess_driver_file(driver_file_name, os.path.join(metadata_dir, m.version))
            full_driver_dir = os.path.join(metadata_dir, m.version, driver_dir)
            # Write detailed build results to args.build_result_dir
            build_results.append(try_build_driver(m, full_driver_dir, args.build_result_dir))
        with open(args.build_json, "w") as bjson:
            bjson.write(json.dumps(build_results, cls=EnhancedJSONEncoder, indent=4))
    else:
        raise RuntimeError("User must specify --metadata_json or --build_json!")
 