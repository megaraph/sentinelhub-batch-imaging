import datetime
import dateutil
import calendar
from evalscript import EVALSCRIPT_TRUE_COLOR
from locations import LOCATION
from catalog_dates import search_catalog
from config import (
    CONFIG, 
    PROJECT_CRS, 
    PROJECT_SATELLITE, 
    IMAGE_RESOLUTION, 
    OUTPUT_DIRECTORY, 
    RANGE, 
    DOWNLOAD_CLIENT,
    OUT_EXT
)
from sentinelhub import (
    BBox,
    DataCollection,
    MimeType,
    SentinelHubRequest,
    bbox_to_dimensions,
    filter_times
)

def extract_multi_images():
    loc_name, aoi_coords = get_coords()

    aoi_bbox = BBox(bbox=aoi_coords, crs=PROJECT_CRS)
    aoi_size = bbox_to_dimensions(aoi_bbox, resolution=IMAGE_RESOLUTION)
    print(f"Image shape at {IMAGE_RESOLUTION} m resolution: {aoi_size} pixels")

    time_interval = get_time_interval(aoi_bbox)
    print(f"\nInterval: {time_interval}\n")

    search_iterator = search_catalog(time_interval, aoi_bbox)
    all_timestamps = search_iterator.get_timestamps()
    time_difference = datetime.timedelta(hours=1)

    unique_acquisitions = filter_times(all_timestamps, time_difference)

    process_requests = []

    for timestamp in unique_acquisitions:
        request_true_color = SentinelHubRequest(
            data_folder=OUTPUT_DIRECTORY,
            evalscript=EVALSCRIPT_TRUE_COLOR,
            input_data=[
                SentinelHubRequest.input_data(
                    data_collection=PROJECT_SATELLITE,
                    time_interval=(timestamp - time_difference, timestamp + time_difference),
                )
            ],
            responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
            bbox=aoi_bbox,
            size=aoi_size,
            config=CONFIG,
        )
        process_requests.append(request_true_color)


    print(f"\nProcessed {len(process_requests)} requests:\n")

    download_requests = [request.download_list[0] for request in process_requests]

    # rename each file to its corresponding date
    for request in download_requests:
        input_data = request.post_values['input']['data'][0]
        data_time_range = input_data['dataFilter']['timeRange']
        data_date = data_time_range['from'].split('T')[0]
        out_filename = f"{loc_name.capitalize()}_{data_date}{OUT_EXT}"
        request.filename = out_filename

    data = DOWNLOAD_CLIENT.download(download_requests, show_progress=True)
    print(f"\n{data[0].shape}\n")

    return None


def get_coords():
    loc = input("Location: ").lower()

    if loc not in LOCATION.keys():
        print("\nWARNING: LOCATION NOT AVAILABLE\n")
        exit()

    return loc, LOCATION[loc]


def get_time_interval(aoi_bbox):
    damage_report_date = input("Enter damage report date [yyyy-mm-dd]: ")
    date_split = [int(el) for el in damage_report_date.split('-')]

    t_year, t_month, t_day = date_split
    month_diff = dateutil.relativedelta.relativedelta(months=RANGE)

    target_date = datetime.date(t_year, t_month, t_day)

    from_date = target_date - month_diff
    to_date = target_date + month_diff


    date_from = str(datetime.date(from_date.year, from_date.month, 1))
    date_to = str(datetime.date(to_date.year, to_date.month, calendar.monthrange(t_year, to_date.month)[1]))

    time_interval = (date_from, date_to)

    return time_interval


if __name__ == "__main__":
    extract_multi_images()
