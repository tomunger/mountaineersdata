import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os
import mtnleaderreport
from pathlib import Path

#
# Set up paths to data directory and report output directory
#
dataDirectory = Path(Path.home(), "Documents/mountaineers/kayak-seattle/leaderactivity")
dataFileName = "Seattle SK Leaders 2018-20v2.csv"
Branch = 'Seattle'
reportDirectory = os.path.join(dataDirectory, "reports")
if not os.path.exists(reportDirectory):
	os.makedirs(reportDirectory)

tripData, earliestDate, latestDate, labelDateRange = mtnleaderreport.loadData(dataDirectory, dataFileName, branch=Branch)



		

#ds_trips = tripData.loc[tripData[mtnleaderreport.H_ACTIVITY_CATEGORY] == 'Trip']
title = 'As Primary Leader'
fileName = os.path.join('.', f"{title}.jpg")
dateRange = mtnleaderreport.fullMonthRange(earliestDate, latestDate)
ds_primaryleader = tripData.loc[tripData[mtnleaderreport.H_ACTIVITY_ROLE] == 'Primary leader']
mtnleaderreport.plotTrips(ds_primaryleader, dateRange, title, fileName)

