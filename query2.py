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

route = "14334"

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
