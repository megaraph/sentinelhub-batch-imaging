from locations import LOCATION
from config import (
    PROJECT_CRS,
    IMAGE_RESOLUTION,
    CONFIG,
    PROJECT_SATELLITE,
    OUTPUT_DIRECTORY,
    PROJECT_OUTPUT_MIMETYPE,
    OUT_EXT,
)
from evalscript import EVALSCRIPT_TRUE_COLOR
from sentinelhub import (
    SentinelHubCatalog,
    SentinelHubRequest,
    BBox,
    bbox_to_dimensions,
)

catalog = SentinelHubCatalog(config=CONFIG)


def get_coords():
    loc = input("Location: ").lower()

    if loc not in LOCATION.keys():
        print("\nWARNING: LOCATION NOT AVAILABLE\n")
        exit()

    return loc, LOCATION[loc]


def get_aoi(bbox, crs=PROJECT_CRS, resolution=IMAGE_RESOLUTION):
    aoi_bbox = BBox(bbox=bbox, crs=crs)
    aoi_size = bbox_to_dimensions(aoi_bbox, resolution=resolution)

    return aoi_bbox, aoi_size, resolution


def search_catalog(time_interval, aoi_bbox):
    search_iterator = catalog.search(
        collection=PROJECT_SATELLITE,
        bbox=aoi_bbox,
        time=time_interval,
        fields={
            "include": [
                "id",
                "properties.datetime",
            ],
            "exclude": [],
        },
    )

    return search_iterator


def get_available_dates(time_interval, aoi_bbox):
    dates = []

    results = list(search_catalog(time_interval, aoi_bbox))

    for result in results:
        result_datetime = result["properties"]["datetime"]
        result_date = result_datetime.split("T")
        dates.append(result_date[0])

    return dates


def get_all_timestamps(time_interval, aoi_bbox):
    search_iterator = search_catalog(time_interval, aoi_bbox)
    all_timestamps = search_iterator.get_timestamps()

    return all_timestamps


def request_true_color(time_interval, bbox, size):
    request_true_color = SentinelHubRequest(
        data_folder=OUTPUT_DIRECTORY,
        evalscript=EVALSCRIPT_TRUE_COLOR,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=PROJECT_SATELLITE,
                time_interval=time_interval,
            )
        ],
        responses=[
            SentinelHubRequest.output_response("default", PROJECT_OUTPUT_MIMETYPE)
        ],
        bbox=bbox,
        size=size,
        config=CONFIG,
    )

    return request_true_color


def update_filename(loc_name, request, ext=OUT_EXT):
    input_data = request.post_values["input"]["data"][0]
    data_time_range = input_data["dataFilter"]["timeRange"]
    data_date = data_time_range["from"].split("T")[0]

    return f"{loc_name.capitalize()}_{data_date}{OUT_EXT}"
