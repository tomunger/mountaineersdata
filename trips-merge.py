'''

Merge trip lists.

Current coded to merge river log into main TripList

'''

import pandas as pd
from pathlib import Path

import trips_river_log


#
# Locaiton of files.
#
TRIPS_DIR = Path(Path.home(), "Documents/trips")
TRIPS_FILE = Path(TRIPS_DIR, "TripList.xlsx")
RIVERS_FILE = Path("River Log.xlsx")

riverdf = trips_river_log.load_river_log(RIVERS_FILE)
print (f"Rivers: {len(riverdf.index)}")


#
# Load the trip list.
#
tripsdf = pd.read_excel(TRIPS_FILE)
print (f"Trips: {len(tripsdf.index)}")

# Save to original file
tripsdf.to_csv("local-merge-trips-1-original.csv", date_format="%Y-%m-%d", index=False)


#
# Append the rivers.
#
tripsdf = tripsdf.append(riverdf, ignore_index=True)
tripsdf.sort_values(by='Date', inplace=True)
tripsdf.reindex()
print (f"Trips merged: {len(tripsdf.index)}")


# Save merged
tripsdf.to_csv("local-merge-trips-2-merged.csv", date_format="%Y-%m-%d", index=False)

