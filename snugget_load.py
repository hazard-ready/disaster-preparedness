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
  globalMode = None  # none for "keep asking for a mode each time"; False for "stop asking"

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
      # go through the new file, replacing or adding as appropriate
      with open(snuggetFile) as csvFile:
        newSnuggets = csv.DictReader(csvFile)
        
        for row in newSnuggets:
#          print(', '.join(row))
#          print(', '.join([row[key] for key in row]))
          # "shapefile" -> world_snugget.shapefile_filter_id column name; store id we just looked up in that column
          filterColumn = row["shapefile"] + "_filter_id"
          # "section" -> world_snugget.section_id
          sectionID = getSectionID(appName, row["section"], cur)
        
          # check if a snugget for this data already exists
          # if we have a lookup value then deal with this value specifically:
          if row["lookup_value"] is not '':  # if it is blank, we'll treat it as matching all existing values
            filterID = findFilterID(appName, row["shapefile"], row["lookup_value"], cur)
            oldSnugget = checkForSnugget(appName, sectionID, filterColumn, filterID, cur)
#            print(oldSnugget)
            mode, globalMode = askUserForMode(row["shapefile"], row["lookup_value"], oldSnugget, [], snuggetFile, globalMode)
            filterIDs = [filterID]  # this will let the rest of the function be the same whether we had one ID or several
          else: 
            filterIDs = findAllFilterIDs(appName, row["shapefile"], cur)
            oldSnuggets = []
            for filterID in filterIDs:
              oldSnugget = checkForSnugget(appName, sectionID, filterColumn, filterID, cur)
              if oldSnugget is not None and oldSnugget not in oldSnuggets:
                oldSnuggets.append(oldSnugget)
#            print(oldSnuggets)
            mode, globalMode = askUserForMode(row["shapefile"], row["lookup_value"], None, oldSnuggets, snuggetFile, globalMode)

          for filterID in filterIDs:
            print(filterID)
            if mode == "replace":  
              # then get the existing snuggetID so we can replace it
              removeOldSnugget(appName, sectionID, filterColumn, filterID, cur)
            addTextSnugget(appName, row, sectionID, filterColumn, filterID, cur)
              
              
              
def addTextSnugget(appName, row, sectionID, filterColumn, filterID, cur):
#   "heading" -> world_textsnugget.heading (null as '')
#   "intensity" -> world_textsnugget.percentage (numeric, null as null)
#   "image" -> world_textsnugget.image
#   "text" -> world_textsnugget.content
  if row["intensity"] == '':
    row["intensity"] = None
  cur.execute(
    'INSERT INTO ' + appName + '_snugget (section_id, "' + filterColumn + '") VALUES (%s, %s);', 
    (str(sectionID), str(filterID))
  )
  snuggetID = getSnuggetID(appName, sectionID, filterColumn, filterID, cur);
  print(row)
  cur.execute(
    'INSERT INTO ' + appName + '_textsnugget (snugget_ptr_id, content, heading, image, percentage) VALUES (%s, %s, %s, %s, %s);',
    (snuggetID, row["text"], row["heading"], row["image"], row["intensity"])
  )



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



def getSnuggetID(appName, sectionID, filterColumn, filterID, cur):
  try:
    cur.execute('SELECT id FROM ' + appName + '_snugget WHERE section_id = ' + str(sectionID) + ' AND "' + filterColumn + '" = ' + str(filterID) + ';')
    return str(cur.fetchone()[0])
  except:
    print(cur.mogrify('SELECT id FROM ' + appName + '_snugget WHERE section_id = ' + str(sectionID) + ' AND "' + filterColumn + '" = ' + str(filterID) + ';'))
    return None




def checkForSnugget(appName, sectionID, filterColumn, filterID, cur):
  # in each of the following DB queries, an empty return means there's no matching snugget
  try:
    snuggetID = getSnuggetID(appName, sectionID, filterColumn, filterID, cur)
    cur.execute("SELECT content FROM " + appName + "_textsnugget WHERE snugget_ptr_id = " + snuggetID + ";")
    return cur.fetchone()[0]
  except:
    return None

  
  
def removeOldSnugget(appName, sectionID, filterColumn, filterID, cur):
  snuggetID = getSnuggetID(appName, sectionID, filterColumn, filterID, cur)
  cur.execute("DELETE FROM " + appName + "_textsnugget WHERE snugget_ptr_id = " + snuggetID + ";")
  cur.execute("DELETE FROM " + appName + "_snugget WHERE id = " + snuggetID + ";")
  print("Removed snugget", snuggetID)
    

  

#TODO: get rid of "add" mode, so it's just a question of replace or quit
def askUserForMode(shapefile, lookup_value, oldSnugget, oldSnuggets, snuggetFile, globalMode):
  if oldSnugget is not None:
    print("In shapefile", shapefile, "there is already a snugget defined for intensity", lookup_value, "with the following text content:")
    print(oldSnugget)
  elif oldSnuggets != []:
    print("In shapefile", shapefile, "there are existing snuggets with the following text content:")
    for snugget in oldSnuggets:
      print(snugget)
  else: # if both oldSnugget and oldSnuggets were empty, then we don't need to ask the user
    return "add", globalMode
  
  if globalMode:
    return globalMode, globalMode
  else:

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
      mode = "add"
    elif response == "R":
      mode = "replace"
    
    if globalMode != False:
      print("Would you like this to apply to all other existing snuggets?")
      print("Y: Yes, apply to all.")
      print("N: No, ask me again next time.")
      print("X: No, and stop asking this question.")
      response = False
      while response not in ["Y", "N", "X"]:
        response = input(">> ").upper()
      
      if response == "Y":
        return mode, mode
      elif response == "N":
        return mode, None

    # if globalMode was either already set to False or the user selected "X" then:
    return mode, False
      





if __name__ == "__main__":
  main()
