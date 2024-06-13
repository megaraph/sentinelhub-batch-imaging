import sys
import datetime
import dateutil
import calendar
from utils import (
    get_coords,
    get_aoi,
    get_all_timestamps,
    request_true_color,
    update_filename,
)
from config import RANGE, DOWNLOAD_CLIENT
from sentinelhub import filter_times


def extract_multiple():
    loc_name, aoi_coords = get_coords()

    aoi_bbox, aoi_size, aoi_res = get_aoi(bbox=aoi_coords)
    print(f"Image shape at {aoi_res} m resolution: {aoi_size} pixels")

    if len(sys.argv) > 1 and sys.argv[1] == "-pm":
        time_interval = get_time_plusminus(aoi_bbox=aoi_bbox)
    else:
        time_interval = get_time_interval(aoi_bbox=aoi_bbox)
    print(f"\nInterval: {time_interval}\n")

    all_timestamps = get_all_timestamps(time_interval=time_interval, aoi_bbox=aoi_bbox)
    time_difference = datetime.timedelta(hours=1)

    unique_acquisitions = filter_times(all_timestamps, time_difference)

    process_requests = []
    for timestamp in unique_acquisitions:
        timestamp_interval = timestamp - time_difference, timestamp + time_difference
        process_requests.append(
            request_true_color(timestamp_interval, aoi_bbox, aoi_size)
        )

    print(f"\nProcessed {len(process_requests)} requests:\n")

    download_requests = [request.download_list[0] for request in process_requests]

    # rename each file to its corresponding date
    for request in download_requests:
        request.filename = update_filename(loc_name=loc_name, request=request)

    data = DOWNLOAD_CLIENT.download(download_requests, show_progress=True)
    print(f"\n{data[0].shape}\n")

    return None


def get_time_interval(aoi_bbox):
    start_date = input("Enter start date [yyyy-mm-dd]: ")
    end_date = input("Enter end date [yyyy-mm-dd]: ")

    start_year, start_month, start_day = [int(el) for el in start_date.split("-")]
    s_date = datetime.date(start_year, start_month, start_day)

    end_year, end_month, end_day = [int(el) for el in end_date.split("-")]
    e_date = datetime.date(end_year, end_month, end_day)

    if e_date < s_date:
        print("End date should not be before start date")
        exit()

    return (str(s_date), str(e_date))


def get_time_plusminus(aoi_bbox):
    damage_report_date = input("Enter damage report date [yyyy-mm-dd]: ")
    date_split = [int(el) for el in damage_report_date.split("-")]

    t_year, t_month, t_day = date_split
    month_diff = dateutil.relativedelta.relativedelta(months=RANGE)

    target_date = datetime.date(t_year, t_month, t_day)

    from_date = target_date - month_diff
    to_date = target_date + month_diff

    date_from = str(datetime.date(from_date.year, from_date.month, 1))
    date_to = str(
        datetime.date(
            to_date.year, to_date.month, calendar.monthrange(t_year, to_date.month)[1]
        )
    )

    time_interval = (date_from, date_to)

    return time_interval


if __name__ == "__main__":
    extract_multiple()
