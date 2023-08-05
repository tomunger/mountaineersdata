import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os
import mtnleaderreport
from pathlib import Path

#
# Set up paths to data directory and report output directory
#
activity = "kayaking"
if activity == "kayaking":
	dataDirectory = Path(Path.home(), "Documents/mountaineers/kayak-seattle/data/leaderactivity")
	dataFileName = "SK Leader Activity-2022-10-05-12-37-20.csv"
elif activity == "hiking":
	dataDirectory = Path(Path.home(), "Documents/mountaineers/hiking/data/")
	dataFileName = "Sea Hike Leader Activity-2021-11-09-09-44-25.csv"
else:
	print ("Unknown activity")
	exit()

Branch = 'Seattle'
reportDirectory = os.path.join(dataDirectory, "reports")
if not os.path.exists(reportDirectory):
	os.makedirs(reportDirectory)



def allActivites(tripdata, roll):
	range17to19 = (datetime.datetime(2015,1,1), datetime.datetime(2020,1,1))
	range20to22 = (datetime.datetime(2020,10,1), datetime.datetime(2022, 10,1))	
	rantepastyear = (datetime.datetime(2020,11,1), datetime.datetime(2021, 11, 11))	
	for dr in [range20to22]:
		ds_datedTrips = ds_primaryleader.loc[ (ds_primaryleader[mtnleaderreport.H_START_DATE] >= dr[0]) & 
					(ds_primaryleader[mtnleaderreport.H_END_DATE] < dr[1]) ]
		ds_datedTrips.info()

		# All Branch
		title = f"All Branchs {roll} - {dr[0]:%Y-%m-%d} to {dr[1]:%Y-%m-%d}"
		print (f"Working on {title}")
		fileName = os.path.join(reportDirectory, f"{title}.jpg")
		mtnleaderreport.plotTrips(ds_datedTrips, dr, title, fileName)

		# Individual branches
		for branch in tripData[mtnleaderreport.H_BRANCH].unique():
			ds_branch = ds_datedTrips.loc[ds_datedTrips[mtnleaderreport.H_BRANCH] == branch]
			title = f"{branch} Branch {roll} - {dr[0]:%Y-%m-%d} to {dr[1]:%Y-%m-%d}"
			print (f"Working on {title}")
			fileName = os.path.join(reportDirectory, f"{title}.jpg")
			mtnleaderreport.plotTrips(ds_branch, dr, title, fileName)


def clinics(tripData, roll):
	dr = (datetime.datetime(2020,1,1), datetime.datetime(2021,10,1))

	ds_datedTrips = tripData.loc[ (tripData[mtnleaderreport.H_START_DATE] >= dr[0]) & 
				(tripData[mtnleaderreport.H_END_DATE] < dr[1]) ]
	ds_datedTrips.info()

	title = f"All Branchs Instructor {roll} - {dr[0]:%Y-%m-%d} to {dr[1]:%Y-%m-%d}"
	print (f"Working on {title}")
	fileName = os.path.join(reportDirectory, f"{title}.jpg")
	mtnleaderreport.plotTrips(ds_datedTrips, dr, title, fileName)


	for branch in tripData[mtnleaderreport.H_BRANCH].unique():
		ds_branch = ds_datedTrips.loc[ds_datedTrips[mtnleaderreport.H_BRANCH] == branch]
		title = f"{branch} Branch Instructor {roll} - {dr[0]:%Y-%m-%d} to {dr[1]:%Y-%m-%d}"
		print (f"Working on {title}")
		fileName = os.path.join(reportDirectory, f"{title}.jpg")
		mtnleaderreport.plotTrips(ds_branch, dr, title, fileName)



tripData, earliestDate, latestDate, labelDateRange = mtnleaderreport.loadData(dataDirectory, dataFileName)
#tripData.info()
		

roll = 'Primary leader'
ds_primaryleader = tripData.loc[tripData[mtnleaderreport.H_ACTIVITY_ROLE] == roll]
allActivites(ds_primaryleader, roll)

#ds_clinics = ds_primaryleader.loc[ (ds_primaryleader[mtnleaderreport.H_ACTIVITY_CATEGORY] == "Clinic") | (ds_primaryleader[mtnleaderreport.H_ACTIVITY_CATEGORY] == "Field Trip") ]
#clinics(ds_clinics, roll)
