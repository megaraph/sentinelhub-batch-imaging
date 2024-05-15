import csv

LOCATION = dict()

with open("src_files/location_extent.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0

    for count, row in enumerate(csv_reader):
        if count == 0:
            continue
        
        loc_name = row[0].lower()
        loc_extent = [float(coordinate) for coordinate in row[1].split(',')]

        LOCATION[loc_name] = loc_extent


