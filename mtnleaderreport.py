import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import datetime
from dateutil.relativedelta import relativedelta
from typing import Tuple
import os

H_BRANCH = "Contact: Branch"
H_FIRST_NAME = "First Name"
H_LAST_NAME = "Last Name"
H_FULL_NAME = "Full Name"
H_ACTIVITY_ROLE = "Activity Role"
H_START_DATE = "Mountaineers Activity: Start Date"
H_END_DATE = "Mountaineers Activity: End Date"
H_ACTIVITY_CATEGORY = "Mountaineers Activity: Activity Category"
H_ACTIVITY_NAME = "Mountaineers Activity: Activity Name"


ACTIVITY_SEMINAR = "Seminar"
ACTIVITY_CLINIC = "Clinic"
ACTIVITY_TRIP = "Trip"
ACTIVITY_FIELDTRIP = "Field Trip"
ACTIVITY_LECTURE = "Lecture"

ACTIVITY_LIST = [ ACTIVITY_TRIP, ACTIVITY_CLINIC, ACTIVITY_FIELDTRIP, ACTIVITY_SEMINAR, ACTIVITY_LECTURE ]

ACTIVITY_COLORMAP = { ACTIVITY_TRIP: "navy", 
					ACTIVITY_CLINIC: "sandybrown", 
					ACTIVITY_FIELDTRIP: "red", 
					ACTIVITY_SEMINAR: "cyan", 
					ACTIVITY_LECTURE: "limegreen" }


def loadData(dataDirectory, dataFileName, branch=None):
	ds = pd.read_csv(os.path.join(dataDirectory, dataFileName)
			, parse_dates=[ H_START_DATE, H_END_DATE ]
			)
	# Filter out subtotal lines:  ds = ds.loc[ds['Contact Plone Id'] != 'Subtotal']
	ds = ds.dropna(subset=[H_LAST_NAME])
	if branch:
		ds = ds.loc[ds[H_BRANCH] == branch]

	# Make a full name field.  
	ds[H_FULL_NAME] = ds[H_FIRST_NAME] + " " + ds[H_LAST_NAME]

	# Find earliest and lateset date.  Make a string describing that range
	earliestDate = ds[H_START_DATE].min()
	latestDate = ds[H_END_DATE].max()
	labelDateRange = f"{earliestDate:%Y-%m-%d} to {latestDate:%Y-%m-%d}"
	return (ds, earliestDate, latestDate, labelDateRange)



def beginningOfMonth(dt) -> datetime.datetime:
	'''Return time at beginning of date.  Timezone information is retained.  
	Returns datetime representing midnight at the start of this day.'''
	return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

def endOfMonth(dt) -> datetime.datetime:
	'''Return time at end of date.  Timezone information is retained.
	Returns datetime representing midnight at the end of this day, which
	is actually start of next day. 
	Time ranges include the beginning time and run up to but not including
	the end time.  So: 
	  beginningOfDay(today) <= X < endOfDay(today)
	captures all times that are part of today.
	'''
	return beginningOfMonth(dt) + relativedelta(months=1)


def fullMonthRange(start,end) -> Tuple[datetime.datetime, datetime.datetime]:
	return (beginningOfMonth(start), endOfMonth(end))

def pdtstodtdt(ts: pd.Timestamp):
	# Convert a Pandas Timestamp to datetime.datetime.
	return datetime.datetime(year=ts.year, month=ts.month, day=ts.day, hour=ts.hour, minute=ts.minute, second=ts.second)


def plotTrips(data: pd.DataFrame, dateRange: Tuple[datetime.datetime, datetime.datetime], title: str, fileName: str):
	ystep = 8
	barHeight = 2


	leaders = data[H_FULL_NAME].unique()
	leaderNameList = []
	leaderCount = len(leaders)
	days = (dateRange[1] - dateRange[0]).days
	
	fig, ax = plt.subplots(figsize=(10+days/33, 1 + leaderCount/2.2))


	leaderNumber = 1
	for leaderName in leaders:
		leaderNameList.append(leaderName)
		trips = data.loc[data[H_FULL_NAME] == leaderName]
		trips = trips.sort_values(by=[H_START_DATE])
		barList = []
		colorList = []
		for index, trip in trips.iterrows():
			dt = trip[H_END_DATE] - trip[H_START_DATE]
			days = dt.days + 1
			dt = datetime.timedelta(days=days)
			barList.append( ( trip[H_START_DATE], dt ) )
			color = ACTIVITY_COLORMAP.get(trip[H_ACTIVITY_CATEGORY], "darkorange")
			colorList.append(color)
		ax.broken_barh(barList, ((leaderNumber*ystep)-barHeight, barHeight*2), facecolors=colorList)
		leaderNumber += 1
	
	ax.set_xlim(dateRange[0], dateRange[1])

	ax.set_ylim(0, (leaderCount+1) * ystep)

	yticks = range(ystep, (leaderCount+1) * ystep, ystep)
	ax.set_yticks(yticks)
	ax.set_yticklabels(leaderNameList)
	xtickList = []
	xt = dateRange[0]
	while xt <= dateRange[1]:
		xtickList.append(xt)
		xt = xt + relativedelta(months=1)
	ax.set_xticks(xtickList)
	ax.set_title(title)
	ax.grid(True)

	legendEntries = []
	for t in ACTIVITY_LIST:
		legendEntries.append(mpatches.Patch(color=ACTIVITY_COLORMAP[t], label=t))
	plt.legend(handles=legendEntries, ncol=len(ACTIVITY_LIST))

	fig.tight_layout()

	if fileName:
		print (f"Saving '{fileName}'")
		plt.savefig(fileName)

	#plt.show()
	plt.close()
