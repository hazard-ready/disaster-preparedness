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
      ''' this section probably redundant now      
      # Find out what's already set up
      sections = readValuesFrom(appName, "snuggetsection", cur)
      subsections = readValuesFrom(appName, "snuggetsubsection", cur)
      oldSnuggets = readValuesFrom(appName, "textsnugget", cur)
      snuggetRefs = readSnuggetCrossRefs(appName, "snugget", cur)
      snuggetColumns = readColumnsFrom(appName, "snugget", cur)
      print(sections)
      print(subsections)
      print(oldSnuggets)
      print(snuggetRefs)
      print(snuggetColumns)
      print("----------")
      #TODO: should I make snuggetRefs into a dict with snuggetColumns as the keys?
      '''      
      
      # Then go through the new file, replacing or adding as appropriate
      with open(snuggetFile) as csvFile:
        newSnuggets = csv.DictReader(csvFile)
        
        for row in newSnuggets:
#          print(', '.join(row))
#          print(', '.join([row[key] for key in row]))
          # shapefile -> world_snugget.shapefile_filter_id column name; store id we just looked up in that column
          filterColumn = row["shapefile"] + "_filter_id"
          # section -> world_snugget.section_id
          sectionId = getSectionID(appName, row["section"], cur)
        
          # check if a snugget for this data already exists
          # if we have a lookup value then deal with this value specifically:
          if row["lookup_value"] is not '':
            filterID = findFilterID(appName, row["shapefile"], row["lookup_value"], cur)
            oldSnugget = checkForSnugget(appName, filterColumn, filterID, row["lookup_value"], cur)
            mode = askUserForMode(row["shapefile"], row["lookup_value"], oldSnugget, [], snuggetFile)
          # otherwise deal with all the possible values, because blank means "apply to all"
          else: 
            filterIDs = findAllFilterIDs(appName, row["shapefile"], cur)
            oldSnuggets = []
            for filterID in filterIDs:
              oldSnugget = checkForSnugget(appName, filterColumn, filterID, row["lookup_value"], cur)
              if oldSnugget is not None and oldSnugget not in oldSnuggets:
                oldSnuggets.append(oldSnugget)
            mode = askUserForMode(row["shapefile"], row["lookup_value"], None, oldSnuggets, snuggetFile)

          #   get id for new row in world_snugget -> world_textsnugget.snugget_ptr_id
          #   heading -> world_textsnugget.heading (null as '')
          #   intensity -> world_textsnugget.percentage (numeric, null as null)
          #   if intensity is blank, should we just generate the same row for all intensities?
          #   image -> world_textsnugget.image
          #   text -> world_textsnugget.content

  
''' these functions probably redundant now
def readValuesFrom(appName, table, cur):
  vals = {}
  cur.execute("SELECT * FROM " + appName + "_" + table.lower() + ";")
  for item in cur.fetchall():
    vals[item[1]] = item[0]
  return vals  





def readSnuggetCrossRefs(appName, table, cur):
  refs = []
  cur.execute("SELECT * FROM " + appName + "_" + table + ";")
  for row in cur.fetchall():
    refs.extend(row)
  return refs
'''

def readColumnsFrom(appName, table, cur):
  cols = []
  cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = '" + appName + "_" + table.lower() + "';")
  for row in cur.fetchall():
    cols.append(row[0])
  return cols





def getSectionID(appName, sectionName, cur):
  cur.execute("SELECT id FROM " + appName + "_snuggetsection WHERE name = '" + sectionName + "';")
  try:
    return cur.fetchone()[0]
  except:
    cur.execute("INSERT INTO " + appName + "_snuggetsection(name) VALUES(%s);", [sectionName])
    cur.execute("SELECT id FROM " + appName + "_snuggetsection WHERE name = '" + sectionName + "';")
    return cur.fetchone()[0]
  
  


def findFilterID(appName, shapefile, key, cur):
  cols = readColumnsFrom(appName, shapefile, cur)
  keyColumn = cols[1]
  cur.execute("SELECT id FROM " + appName + "_" + shapefile + " WHERE " + keyColumn + "::text = '" + key + "';")
  return str(cur.fetchone()[0])

    
    
def findAllFilterIDs(appName, shapefile, cur):
  ids = []
  cur.execute("SELECT id FROM " + appName + "_" + shapefile + ";")
  for row in cur.fetchall():
    ids.extend(row)
  return ids
  


def checkForSnugget(appName, filterColumn, filterID, key, cur):
  # in each of the following DB queries, an empty return means there's no matching snugget
  try:
    cur.execute('SELECT id FROM ' + appName + '_snugget WHERE "' + filterColumn + '" = ' + filterID + ';')
    snuggetID = str(cur.fetchone()[0])
    cur.execute("SELECT content FROM " + appName + "_textsnugget WHERE snugget_ptr_id = " + snuggetID + ";")
    return cur.fetchone()[0]
  except:
    return None

  
  
  
def askUserForMode(shapefile, lookup_value, oldSnugget, oldSnuggets, snuggetFile):
  if oldSnugget is not None:
    print("In shapefile", shapefile, "there is already a snugget defined for intensity", lookup_value, "with the following text content:")
    print(oldSnugget)
  elif oldSnuggets != []:
    print("In shapefile", shapefile, "there are existing snuggets with the following text content:")
    for snugget in oldSnuggets:
      print(snugget)
  else: # if both oldSnugget and oldSnuggets were empty, then we don't need to ask the user
    return "add"
    
  print("Please enter one of the following letters to choose how to proceed:")
  print("A: add a new snugget, in addition to the existing one.")
  print("R: replace the old snugget with the new value loaded from", snuggetFile)
  print("Q: quit so you can edit", snuggetFile, "and try again.")

  response = False
  while response not in ["A", "R", "Q"]:
    response = input(">> ").upper()
  
  if response == "Q":
    exit(0)
  elif response == "A":
    return "add"
  elif response == "R":
    return "replace"





if __name__ == "__main__":
  main()
