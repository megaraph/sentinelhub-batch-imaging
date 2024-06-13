import datetime
import calendar
from config import CONFIG, OUTPUT_DIRECTORY
from evalscript import EVALSCRIPT_TRUE_COLOR
from locations import LOCATION
from utils import get_available_dates, get_aoi, request_true_color, get_coords
from sentinelhub import DataCollection, MimeType, SentinelHubRequest


def extract_single():
    aoi_coords = get_coords()

    aoi_bbox, aoi_size, aoi_res = get_aoi(bbox=aoi_coords)
    print(f"Image shape at {aoi_res} m resolution: {aoi_size} pixels")

    time_interval = get_time_interval(aoi_bbox)

    request = request_true_color(
        time_interval=time_interval, bbox=aoi_bbox, size=aoi_size
    )

    request.get_data(save_data=True)

    return None


def get_time_interval(aoi_bbox):
    target_date = input("Enter year-month timeline [yyyy-mm]: ")
    date_split = [int(el) for el in target_date.split("-")]
    t_year, t_month = date_split

    time_interval = datetime.date(t_year, t_month, 1), datetime.date(
        t_year, t_month, calendar.monthrange(t_year, t_month)[1]
    )

    dates = get_available_dates(time_interval, aoi_bbox)
    print(f"\nTotal of {len(dates)} available dates:\n")
    print(dates)

    t_day = int(input("Enter day [dd]: "))

    date_from = datetime.datetime(t_year, t_month, t_day, 0, 0)
    date_to = date_from + datetime.timedelta(hours=23, minutes=59)

    time_interval = (date_from, date_to)
    return time_interval


if __name__ == "__main__":
    extract_single()
