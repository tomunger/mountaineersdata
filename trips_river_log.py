'''
Load my river log.  This is kept in a google sheet.  Download as an Excel file.

Manually keep track of what has been imported in a 'Imported' column.
'''
import pandas as pd
from pathlib import Path
import re





def load_river_log(file: Path) -> pd.DataFrame:
       mtndf = pd.DataFrame(columns=['Trip', 'Route', 'Date', 'Days', 'Dist', 'Type', 'SubType', 'Result', 'Group', 'Src', 
         'Notes', 'Ldr', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6'])

       rldf = pd.read_excel(file)

       

       for index, row in rldf.iterrows():

              if row["Imported"] == "Y":
                     continue
              
              if not pd.isna(row["Section"]):
                     route = f"{row['Section']} ({row['Put-in']} - {row['Take-Out']})"
              else:
                     route = f"{row['Put-in']} - {row['Take-Out']}"

              days = None
              if not pd.isna(row['Time']):
                     m = re.match(r"(\d+)\s+days", str(row['Time']), re.IGNORECASE)
                     if m is not None:
                            days = m.group(1)
              if days is None:
                     days = 1

              notes = row['Notes'] if not pd.isna(row['Notes']) else ''
              if not pd.isna(row['Gauge']):
                     notes += f"  Gauge {row['Gauge']} at {row['Flow']}"

              distance = ''
              if not pd.isna(row['Distance']):
                     distance = row['Distance']

              mtndf = mtndf.append({
                     'Trip': row["River"], 
                     'Route': route, 
                     'Date': row["Date"], 
                     'Days': days, 
                     'Dist' : distance,
                     'Type': "River", 
                     'SubType': "Packraft", 
                     'Result': "Completed", 
                     'Group': "Private",
                     'Src' : 'R',
                     'Notes': notes, 
                     'Ldr': "Tom Unger"
              }, ignore_index=True)

       return mtndf.sort_values ('Date')

