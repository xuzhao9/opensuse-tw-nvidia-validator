# opensuse-tw-nvidia-validator

Validate the compatibility between openSUSE Tumbleweed snapshots and NVIDIA driver

## Usage

### Step 1: Download the drivers

Use the following command to download the most recent 3 NVIDIA Linux
drivers, and save the index in `metadata.json`.

```
python opensuse_tw_nvidia_validator/nvidia-driver-inspector.py -n 3 --metadata-json $PWD/.workdir/metadata.json --download
```

An example of `metadata.json` file looks like the following:

```
[
    {
        "version": "545.29.02",
        "release_date": "20231031"
    },
    {
        "version": "535.129.03",
        "release_date": "20231031"
    },
    {
        "version": "525.147.05",
        "release_date": "20231031"
    }
]
```

The data is retrieved from the URL `https://www.nvidia.com/en-us/drivers/unix/linux-amd64-display-archive/`.

### Step 2: Try build the kernel module

Use the following command to unpack each of the NVIDIA driver in the metadata file, then try building it against the current Linux kernel.

```
python opensuse_tw_nvidia_validator/nvidia-driver-inspector.py --metadata-json $PWD/.workdir/metadata.json --build-json $PWD/.workdir/build.json
```

An example of the output build json output:

```
[
    {
        "metadata": {
            "version": "545.29.02",
            "release_date": "20231031"
        },
        "opensuse_snapshot_version": "20231117",
        "kernel_version": "6.6.1-1-default",
        "build_status": "success"
    },
    {
        "metadata": {
            "version": "535.129.03",
            "release_date": "20231031"
        },
        "opensuse_snapshot_version": "20231117",
        "kernel_version": "6.6.1-1-default",
        "build_status": "success"
    },
    {
        "metadata": {
            "version": "525.147.05",
            "release_date": "20231031"
        },
        "opensuse_snapshot_version": "20231117",
        "kernel_version": "6.6.1-1-default",
        "build_status": "success"
    }
]
```
