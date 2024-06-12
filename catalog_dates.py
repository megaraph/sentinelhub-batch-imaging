from sentinelhub import SentinelHubCatalog, DataCollection
from config import CONFIG, PROJECT_SATELLITE

catalog = SentinelHubCatalog(config=CONFIG)

def search_catalog(time_interval, aoi_bbox):
    search_iterator  = catalog.search(
        collection=PROJECT_SATELLITE,
        bbox=aoi_bbox,
        time=time_interval,
        fields={"include": ["id", "properties.datetime",], "exclude": []},
    )

    return search_iterator

def get_available_dates(time_interval, aoi_bbox):
    dates = []

    results = list(search_catalog(time_interval, aoi_bbox))

    for result in results:
        result_datetime = result["properties"]["datetime"]
        result_date = result_datetime.split('T')
        dates.append(result_date[0])
    
    return dates
    
