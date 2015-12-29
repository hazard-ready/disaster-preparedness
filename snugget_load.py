import os
import csv

import psycopg2

# I think this should eventually be rolled into import.py, along with the makemigrations, migrate and load.run() steps
# but for now it's easier to develop as a separate script
def main():
  appName = "world"
  appDir = "world"
  dataDir = os.path.join(appDir, "data")
  snuggetFile = os.path.join(dataDir, "snuggets.csv")

  try:
    dbURL = os.environ['DATABASE_URL']
  except:
    print("Error: DATABASE_URL environment variable is not set. See README.md for how to set it.")
    exit()
  
# dbURL should be in the form protocol://user:password@host:port/databasename  
  dbParts = [x.split('/') for x in dbURL.split('@')]
  dbHost = dbParts[1][0].split(":")[0]
  dbPort = dbParts[1][0].split(":")[1]
  dbUser = dbParts[0][2].split(":")[0]
  dbPass = dbParts[0][2].split(":")[1]
  dbName = dbParts[1][1]
  
  with psycopg2.connect(host=dbHost, port=dbPort, user=dbUser, password=dbPass, database=dbName) as conn:
    with conn.cursor() as cur:
      # Find out whats already set up
      sections = readValuesFrom(appName, "snuggetsection", cur)
      subsections = readValuesFrom(appName, "snuggetsubsection", cur)
      oldSnuggets = readValuesFrom(appName, "textsnugget", cur)
      snuggetRefs = readSnuggetCrossRefs(appName, "snugget", cur)
      snuggetColumns = readColumnsFrom(appName, "snugget", cur)
      print(snuggetRefs)
      print(snuggetColumns)
      #TODO: should I make snuggetRefs into a dict with snuggetColumns as the keys?
      
      # Then go through the new file, replacing or adding as appropriate
      with open(snuggetFile) as csvFile:
        newSnuggets = csv.DictReader(csvFile)
        
        for row in newSnuggets:
          print(', '.join(row))

  

def readValuesFrom(appName, table, cur):
  vals = {}
  cur.execute("SELECT * FROM " + appName + "_" + table + ";")
  for item in cur.fetchall():
    vals[item[1]] = item[0]
  return vals  




def readColumnsFrom(appName, table, cur):
  cols = []
  cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = '" + appName + "_" + table + "';")
  for row in cur.fetchall():
    cols.append(row[0])
  return cols




def readSnuggetCrossRefs(appName, table, cur):
  refs = []
  cur.execute("SELECT * FROM " + appName + "_" + table + ";")
  for row in cur.fetchall():
    refs.extend(row)
  return refs



if __name__ == "__main__":
  main()
