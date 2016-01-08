import os
import csv

import psycopg2

def main():
  appName = "world"
  appDir = "world"
  dataDir = os.path.join(appDir, "data")
  snuggetFile = os.path.join(dataDir, "snuggets.csv")
  overwriteAll = False

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
      with open(snuggetFile) as csvFile:
        newSnuggets = csv.DictReader(csvFile)
        for row in newSnuggets:
          overwriteAll = processRow(appName, snuggetFile, cur, overwriteAll, row)


          

          
def processRow(appName, snuggetFile, cur, overwriteAll, row):
  filterColumn = row["shapefile"] + "_filter_id"
  sectionID = getSectionID(appName, row["section"], cur)

  # check if a snugget for this data already exists
  # if we have a lookup value then deal with this value specifically:
  if row["lookup_value"] is not '':  # if it is blank, we'll treat it as matching all existing values
    filterIDs = [findFilterID(appName, row["shapefile"], row["lookup_value"], cur)]
    oldSnugget = checkForSnugget(appName, sectionID, filterColumn, filterIDs[0], cur)
    overwriteAll = askUserAboutOverwriting(row, oldSnugget, [], snuggetFile, overwriteAll)
  else: 
    filterIDs = findAllFilterIDs(appName, row["shapefile"], cur)
    oldSnuggets = []
    for filterID in filterIDs:
      oldSnugget = checkForSnugget(appName, sectionID, filterColumn, filterID, cur)
      if oldSnugget is not None and oldSnugget not in oldSnuggets:
        oldSnuggets.append(oldSnugget)
    overwriteAll = askUserAboutOverwriting(row, None, oldSnuggets, snuggetFile, overwriteAll)

  for filterID in filterIDs:
    removeOldSnugget(appName, sectionID, filterColumn, filterID, cur)
    addTextSnugget(appName, row, sectionID, filterColumn, filterID, cur)
  
  return overwriteAll
              
              
             
          
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
  cur.execute(
    'INSERT INTO ' + appName + '_textsnugget (snugget_ptr_id, content, heading, image, percentage) VALUES (%s, %s, %s, %s, %s);',
    (snuggetID, row["text"], row["heading"], row["image"], row["intensity"])
  )



def readColumnsFrom(appName, table, cur):
  cols = []
  cur.execute(
    "SELECT column_name FROM information_schema.columns WHERE table_name = %s;", 
    [appName + "_" + table.lower()]
  )
  for row in cur.fetchall():
    cols.append(row[0])
  return cols





def getSectionID(appName, sectionName, cur):
  cur.execute("SELECT MIN(id) FROM " + appName + "_snuggetsection WHERE name = %s;", [sectionName])
  sectionID = cur.fetchone()[0]
  if sectionID is not None:
    return sectionID
  else: # if no sectionID was found then we need to create the section
    cur.execute("INSERT INTO " + appName + "_snuggetsection(name) VALUES(%s);", [sectionName])
    cur.execute("SELECT id FROM " + appName + "_snuggetsection WHERE name = %s;", [sectionName])
    sectionID = cur.fetchone()[0]
    return sectionID
  
  


def findFilterID(appName, shapefile, key, cur):
  cols = readColumnsFrom(appName, shapefile, cur)
  keyColumn = cols[1]
  cur.execute("SELECT id FROM " + appName + "_" + shapefile + " WHERE " + keyColumn + "::text = %s;", [key])
  return str(cur.fetchone()[0])

    
    
def findAllFilterIDs(appName, shapefile, cur):
  ids = []
  cur.execute("SELECT id FROM " + appName + "_" + shapefile + ";")
  for row in cur.fetchall():
    ids.extend(row)
  return ids



def getSnuggetID(appName, sectionID, filterColumn, filterID, cur):
  cur.execute(
    'SELECT MAX(id) FROM ' + appName + '_snugget WHERE section_id = %s AND "' + filterColumn + '" = %s;',
    (sectionID, filterID)
  )
  snuggetID = cur.fetchone()[0]
  if snuggetID is not None:
    return str(snuggetID)
  else:
    return None




def checkForSnugget(appName, sectionID, filterColumn, filterID, cur):
  try:
    snuggetID = getSnuggetID(appName, sectionID, filterColumn, filterID, cur)
    cur.execute("SELECT content FROM " + appName + "_textsnugget WHERE snugget_ptr_id = %s;", [snuggetID])
    return cur.fetchone()[0]
  except: # if nothing came back from the DB, just return None rather than failing
    return None

  
  
def removeOldSnugget(appName, sectionID, filterColumn, filterID, cur):
  snuggetID = getSnuggetID(appName, sectionID, filterColumn, filterID, cur)
  if snuggetID is not None:
    cur.execute("DELETE FROM " + appName + "_textsnugget WHERE snugget_ptr_id = %s;", [snuggetID])
    cur.execute("DELETE FROM " + appName + "_snugget WHERE id = %s;", [snuggetID])
    print("Replacing snugget", snuggetID)
    

  


# Check with the user about overwriting existing snuggets, giving them the options to:
# either quit and check what's going on, or say "yes to all" and not get prompted again.
def askUserAboutOverwriting(row, oldSnugget, oldSnuggets, snuggetFile, overwriteAlreadySet):
  if overwriteAlreadySet: # if it's already set, then don't do anything else
    return True
  else:
    if oldSnugget is not None:
      print("In shapefile ", repr(row["shapefile"]), " there is already a snugget defined for section " , repr(row["section"]), ", subsection ", repr(row["subsection"]), ", intensity ", repr(row["lookup_value"]), " with the following text content:", sep="")
      print(oldSnugget)
    elif oldSnuggets != []:
      print("In shapefile ", repr(row["shapefile"]), " there are existing snuggets for section" , repr(row["section"]), ", subsection ", repr(row["subsection"]), " with the following text content:", sep="")
      for snugget in oldSnuggets:
        print(snugget)
    else: 
      # if no existing snuggets were found, then we neither need to ask the user this time nor change overwriteAll in the calling function
      return overwriteAlreadySet

    print("Please enter one of the following letters to choose how to proceed:")
    print("R: Replace the existing snugget[s] with the new value loaded from", snuggetFile, " and ask again for the next one.")
    print("A: replace All without asking again.")
    print("Q: quit so you can edit", snuggetFile, "and/or check the snuggets in the Django admin panel and try again.")
    response = ""
    while response not in ["A", "R", "Q"]:
      response = input(">> ").upper()

    if response == "Q":
      exit(0)
    elif response == "A":
      return True
    elif response == "R":
      return False

      





if __name__ == "__main__":
  main()
