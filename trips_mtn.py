'''
Process a CSV file copied from my mountaineer's activities page.

Required some hand editing.  There are non-standard space charcters which I converted to standard.

'''
import pandas as pd
from pathlib import Path
import csv
import datetime
import re

TRIPS_DIR = Path(Path.home(), "Documents/trips")
TRIPS_MTN_FILE = Path(TRIPS_DIR, "TripList-Mountaineers.csv")





def parsedate(date: str) -> datetime.date:
	'''Convert date string to date object.'''
	# Dates come in two formats.
	if '-' in date:
		dt = datetime.datetime.strptime(date, "%Y-%m-%d")
	else:
		dt = datetime.datetime.strptime(date, "%b %d, %Y")
	return dt

# Pattern to split the "activity - event" field.
aere = re.compile(r"^(.+) - (.+)$")

# Pattern to split the "Role: result" field.
rore = re.compile(r"^(.+): (.+)$")

# Map activities to my type and subtype
activityMap = {"Sea Kayak": ("Kayak", "Sea"),
		"Sea Kayak - Wet Wednesday": ("Kayak", "Sea"),
		"Strokes and Manuevers": ("Kayak", "Sea"),
		"Wet Wednesday": ("Kayak", "Sea"),
		"Basic Alpine Climb": ("Climb", "Rock"),
		"Boat Control Clinic": ("Kayak", "Sea"),
		"Essential Sea Kayak Skills": ("Kayak", "Sea"),
		"FLOW - Fun and Learning on the Water": ("Kayak", "Sea"),
		"FLOW- Fun & Learning on the Water": ("Kayak", "Sea"),
		"Kayak Roll Class - Seattle": ("Kayak", "Sea"),
		"Kayak Roll Coaching - Small Group": ("Kayak", "Sea"),
		"Maneuvering strokes": ("Kayak", "Sea"),
		"Paddling in Moving Water": ("Kayak", "Sea"),
		"Paddling in Moving Water at Deception Pass": ("Kayak", "Sea")
	}

# Map climbing outcomes to my climbing outcomes
climbOutcome = { "Successful": "Summited", "Turned Around": "Retreated" }

# Map sea kayak outcomes to my outcomes.
outcomeMap = { "Successful": "Completed", "Turned Around": "Incomplete" }



def load_mtn_activity() -> pd.DataFrame:
	# Create an empty dataframe with columns matching my personal trip list.
	mtndf = pd.DataFrame(columns=['Trip', 'Route', 'Date', 'Days', 'Type', 'SubType', 'Result', 'Group', 'Mtn', 
		'Notes', 'Ldr', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6'])

	with open(TRIPS_MTN_FILE,"r", encoding='utf-8') as fp:
		# Open CSV reader and dispose of two heaeder columns
		csvFile = csv.reader(fp)
		csvFile.__next__()		
		csvFile.__next__()
		try: 
			while True:
				line = csvFile.__next__()

				

				# Parse the date
				# One day trips have a single date while two day trips have a first day and last day.
				# In the case of two day trip, the first date has a ' -' at the end and the second
				# date is on the next line.
				if line[0].endswith(' -'):
					startDate = parsedate(line[0][:-2])			# Parse start date with out trailing ' -'
					line2 = csvFile.__next__()					# Get next line contianing the end date
					endDate = parsedate(line2[0])
					td = endDate - startDate					
					days = td.days + 1							# Calculate the number of days.
				else:
					startDate = parsedate(line[0])
					days = 1

				# Split the activity and event.
				m = aere.match(line[1])
				if m:
					activity = m.group(1)
					subactivity = m.group(2)
				else:
					# In case there is a value that does not follow standard format, use complete field.
					activity = line[1]
					subactivity = ""

				# Convert activity into my standard type.  
				activityInfo = activityMap.get(activity)
				if activityInfo is None:
					# If I dont' have a mapping, this is not a trip.  It is some in-city event.
					continue


				leader = line[2]

				outcome = line[3]
				if outcome == 'Canceled':
					continue

				route = ''
				if activityInfo[0] == "Climb":
					# This is a climbing activity.
					outcome = climbOutcome[outcome]
					# The subactivity field contains "Peak name/Route"
					# So split those out 
					subsubactivity = subactivity.split("/",maxsplit=2)
					subactivity = subsubactivity[0]
					route = subsubactivity[1]

				else: 
					outcome = outcomeMap[outcome]

				mtndf = mtndf.append({
						'Trip': subactivity, 
						'Route': route, 
						'Date': startDate, 
						'Days': days, 
						'Type': activityInfo[0], 
						'SubType': activityInfo[1], 
						'Result': outcome, 
						'Group': "Mountaineers",
						'Mtn' : 'Y',
						'Notes': activity, 
						'Ldr': leader
				}, ignore_index=True)

		except StopIteration:
			pass

	return mtndf.sort_values(by='Date')
	

#mtndf = load_mtn_activity()
