import getpass
import irisnative

user = input("IRIS user: ")
password = getpass.getpass("IRIS password: ")
conn = irisnative.createConnection("127.0.0.1", 51773, "USER", user, password)
iris = irisnative.createIris(conn)

stop_id = None

stop_name = "Silver Ave & Holyoke St"
stop_id = iris.get("stopnames", stop_name)
if stop_id is None:
    print("Stop not found.")
    import sys
    sys.exit()

route_short_name = "44"
route = None

types = iris.iterator("routes").subscripts()
for type in types:
    route_ids = iris.iterator("routes", type).subscripts()
    for route_id in route_ids:
        if iris.isDefined("routes", type, route_id, route_short_name) == 1:
            route = route_id

if route is None:
    print("No route found.")
    import sys
    sys.exit()

selected_trips = set()

directions = iris.iterator("trips", route).subscripts()
for direction in directions:
    selected_trips.update(iris.iterator("trips", route, direction).subscripts())

all_stop_times = set()

for trip in selected_trips:
    all_stop_times.update(iris.iterator("stoptimes", stop_id, trip).values())

for stop_time in sorted(all_stop_times):
    print(stop_time)

conn.close()
