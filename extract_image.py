import datetime
import calendar
import os
import numpy as np
from config import CONFIG, PROJECT_CRS, IMAGE_RESOLUTION, OUTPUT_DIRECTORY
from evalscript import EVALSCRIPT_TRUE_COLOR
from locations import LOCATION
from catalog_dates import get_available_dates
from sentinelhub import (
    BBox,
    DataCollection,
    MimeType,
    SentinelHubRequest,
    bbox_to_dimensions,
)

def extract_image():
    aoi_coords = get_coords()

    aoi_bbox = BBox(bbox=aoi_coords, crs=PROJECT_CRS)
    aoi_size = bbox_to_dimensions(aoi_bbox, resolution=IMAGE_RESOLUTION)
    print(f"Image shape at {IMAGE_RESOLUTION} m resolution: {aoi_size} pixels")

    time_interval = get_time_interval(aoi_bbox)

    request_true_color = SentinelHubRequest(
        data_folder=OUTPUT_DIRECTORY,
        evalscript=EVALSCRIPT_TRUE_COLOR,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L2A,
                time_interval=time_interval,
            )
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
        bbox=aoi_bbox,
        size=aoi_size,
        config=CONFIG,
    )

    request_true_color.get_data(save_data=True)

    return None


def get_coords():
    loc = input("Location: ").lower()

    if loc not in LOCATION.keys():
        print("\nWARNING: LOCATION NOT AVAILABLE\n")
        exit()

    return LOCATION[loc]


def get_time_interval(aoi_bbox):
    target_date = input("Enter year-month timeline [yyyy-mm]: ")
    date_split = [int(el) for el in target_date.split('-')]
    t_year, t_month = date_split

    time_interval = datetime.date(t_year, t_month, 1), datetime.date(t_year, t_month, calendar.monthrange(t_year, t_month)[1])

    dates = get_available_dates(time_interval, aoi_bbox)
    print(f"\nTotal of {len(dates)} available dates:\n")
    print(dates)

    t_day = int(input("Enter day [dd]: "))

    date_from = datetime.datetime(t_year, t_month, t_day, 0, 0)
    date_to =  date_from + datetime.timedelta(hours=23, minutes=59)

    time_interval = (date_from, date_to)
    return time_interval


if __name__ == "__main__":
    extract_image()
