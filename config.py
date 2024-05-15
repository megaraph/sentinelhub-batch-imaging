import os
from sentinelhub import SHConfig, CRS, SentinelHubDownloadClient

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']

if not CLIENT_ID or not CLIENT_SECRET:
    raise Exception("Warning! To use Process API, please provide the credentials (OAuth client ID and client secret).")

CONFIG = SHConfig(
    sh_client_id=CLIENT_ID,
    sh_client_secret=CLIENT_SECRET,
)

if not CONFIG.sh_client_id or not CONFIG.sh_client_secret:
    raise Exception("Warning! To use Process API, please provide the credentials (OAuth client ID and client secret).")


DOWNLOAD_CLIENT = SentinelHubDownloadClient(config=CONFIG)

# Other options: https://sentinelhub-py.readthedocs.io/en/latest/reference/sentinelhub.constants.html#sentinelhub.constants.CRS
PROJECT_CRS = CRS.POP_WEB

# Measured in meters
IMAGE_RESOLUTION = 5

# To store downloded images
OUTPUT_DIRECTORY = "output"

# DAMAGE REPORT MONTH RANGE
RANGE = 2
