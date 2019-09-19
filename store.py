import csv
import irisnative
import getpass

user = input("IRIS user: ")
password = getpass.getpass("IRIS password: ")
conn = irisnative.createConnection("127.0.0.1", 51773, "USER", user, password)
iris = irisnative.createIris(conn)

with open("stops.txt", "r") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Ignore column names

    # stops -> [stop_id]=[stop_name]
    for row in reader:
        iris.set(row[6], "stops", row[4])

with open("routes.txt", "r") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Ignore column names

    # routes -> [route_type] -> [route_id] -> [route_short_name]=[route_long_name]
    for row in reader:
        iris.set(row[0], "routes", row[1], row[5], row[8])

with open("trips.txt", "r") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Ignore column names

    # trips -> [route_id] -> [direction_id]=[trip_headsign] ->[trip_id]
    for row in reader:
        iris.set(row[3], "trips", row[1], row[2])
        iris.set(None, "trips", row[1], row[2], row[6])

with open("stop_times.txt", "r") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Ignore column names

    # stoptimes -> [stop_id] -> [trip_id] -> [stop_sequence]=[departure_time]
    for row in reader:
        iris.set(row[2], "stoptimes", row[3], row[0], row[4])

iter = iris.iterator("stops").items()
for item in iter:
    iris.set(item[0], "stopnames", item[1])
