import os
import csv

from django.core.files import File
from django.contrib.contenttypes.models import ContentType
from disasterinfosite.models import *

currentPath = os.path.dirname(__file__)
appName = "disasterinfosite"
appDir = os.path.join(currentPath, "disasterinfosite")
dataDir = os.path.join(appDir, "data")
snuggetFile = os.path.join(dataDir, "snuggets.csv")

requiredFields = ['shapefile', 'section', 'subsection']
# all other fields in snuggetFile are required. The empty string is to deal with Excel's charming habit of putting a blank column after all data in a CSV.
optionalFields = ['heading', 'intensity', 'image', 'lookup_value', 'txt_location', 'pop_out_image', 'pop_out_link','pop_alt_txt', 'pop_out_txt', 'intensity_txt', 'text', 'image_slideshow_folder', 'video', '']

def run():
  overwriteAll = False

  with open(snuggetFile) as csvFile:
    newSnuggets = csv.DictReader(csvFile)
    rowCount = 1 # row 1 consists of field names, so row 2 is the first data row. We'll increment this before first referencing it.
    for row in newSnuggets:
      rowCount += 1
      if allRequiredFieldsPresent(row, rowCount):
        overwriteAll = processRow(row, overwriteAll)

  print("Snugget load complete. Processed", rowCount, "rows in", snuggetFile)


def allRequiredFieldsPresent(row, rowCount):
  if any(a != '' for a in row.values()): # if the entire row is not empty
    blanks = []
    for key in row.keys():
      if (key not in optionalFields) and (row[key] == ''):
        blanks.append(key)
    if blanks == []:
      return True
    else:
      print("Unable to process row", rowCount, "with content:")
      print(row)
      if len(blanks) > 1:
        print("Because required fields", blanks, "are empty.")
      else:
        print("Because required field", "'" + blanks[0] + "'", "is empty.")
      return False
  else: # the entire row is blank
    print("Skipping empty row", rowCount)
    return False


def processRow(row, overwriteAll):
  shapefile = getShapefileClass(row)
  filterColumn = row["shapefile"] + "_filter"
  section, created = SnuggetSection.objects.get_or_create(name=row["section"])

  if created:
    print("Created a new snugget section: ", row["section"])

  # check if a snugget for this data already exists
  # if we have a lookup value then deal with this value specifically:
  if row["lookup_value"] is not '':  # if it is blank, we'll treat it as matching all existing values
    filterVal = row["lookup_value"]
    oldSnugget = checkForSnugget(shapefile, section, filterColumn, filterVal)
    overwriteAll = askUserAboutOverwriting(row, oldSnugget, overwriteAll)
    processSnugget(row, shapefile, section, filterColumn, filterVal)
    return overwriteAll
  else:
    filterVals = findAllFilterVals(shapefile)
    oldSnuggets = []
    for filterVal in filterVals:
      if filterVal is None:
        print("Skipping row:")
        print(row)
        print("Because no filter for lookup_value", row["lookup_value"], "was found in", row["shapefile"])
        return overwriteAll
      else:
        oldSnugget = checkForSnugget(shapefile, section, filterColumn, filterVal)
        if oldSnugget is not None and oldSnugget not in oldSnuggets:
          oldSnuggets.append(oldSnugget)
      overwriteAll = askUserAboutOverwriting(row, oldSnuggets, overwriteAll)
      processSnugget(row, shapefile, section, filterColumn, filterVal)

    return overwriteAll


def processSnugget(row, shapefile, section, filterColumn, filterVal):
  removeOldSnugget(shapefile, section, filterColumn, filterVal)
  if row["image_slideshow_folder"] is not '':
    addSlideshowSnugget(row, shapefile, section, filterColumn, filterVal)
  elif row["video"] is not '':
    addVideoSnugget(row, shapefile, section, filterColumn, filterVal)
  else:
    addTextSnugget(row, shapefile, section, filterColumn, filterVal)



def getShapefileClass(row):
  modelName = row["shapefile"].lower()
  if ContentType.objects.filter(app_label=appName, model=modelName).exists():
    shapefile = ContentType.objects.get(app_label=appName, model=modelName).model_class()
    return shapefile
  else:  # this means that nothing was found in the database for the shapefile name we read from snuggetFile
    print("No shapefile with the name", row["shapefile"], "appears to have been loaded.")
    print("If the shapefile exists, you may still need to run the migration and loading steps - see the 'Load some data' section of the readme file.")
    return None


def getFilterFieldName(shapefile):
  # The lookup value / filter field is the one from the shapefile that is not one of these.
  field = next(f for f in shapefile._meta.get_fields() if f.name not in ['id', 'geom', 'group'])
  return field.name


def getShapefileFilter(shapefile, filterVal):
  fieldName = getFilterFieldName(shapefile)
  kwargs = {fieldName: filterVal}
  if shapefile.objects.filter(**kwargs).exists():
    return shapefile.objects.get(**kwargs)
  else:
    print("Could not find a filter field for", shapefile)
    return None


def addPopOutIfExists(row):
  if (row["pop_out_image"] != '' or row["pop_out_txt"] != '' or row["pop_alt_txt"] != '' or row["pop_out_link"] != ''):
    print('Creating pop-out section with values ', row["pop_out_image"], row["pop_out_txt"], row["pop_alt_txt"], row["pop_out_link"] )
    popout = SnuggetPopOut.objects.create(text=row["pop_out_txt"], alt_text=row["pop_alt_txt"], link=row["pop_out_link"])
    if row["pop_out_image"] != '':
      imageFile = os.path.join(dataDir, 'images/pop_out', row["pop_out_image"])
      with open(imageFile, 'rb') as f:
        data = File(f)
        popout.image.save(row["pop_out_image"], data, True)

    return popout
  else:
    return None



def addTextSnugget(row, shapefile, section, filterColumn, filterVal):
#   "intensity" -> disasterinfosite_textsnugget.percentage (numeric, null as null)
#   "text" -> disasterinfosite_textsnugget.content
#   "heading" -> disasterinfosite_textsnugget.display_name
  if row["intensity"] == '':
    row["intensity"] = None
  group = shapefile.getGroup()
  shapefileFilter = getShapefileFilter(shapefile, filterVal)

  kwargs = {
  'section': section,
  'group': group,
  filterColumn: shapefileFilter,
  'content': row["text"],
  'percentage': row["intensity"],
  }
  print('creating text snugget with:', kwargs)
  snugget = TextSnugget.objects.create(**kwargs)
  snugget.pop_out = addPopOutIfExists(row)
  snugget.save()


def addVideoSnugget(row, shapefile, section, filterColumn, filterVal):
  pass


def addSlideshowSnugget(row, shapefile, section, filterColumn, filterVal):
  if row["intensity"] == '':
    row["intensity"] = None
  group = shapefile.getGroup()
  shapefileFilter = getShapefileFilter(shapefile, filterVal)

  kwargs = {
  'section': section,
  'group': group,
  filterColumn: shapefileFilter,
  'text': row["text"],
  }
  print('creating slideshow snugget with:', kwargs)
  snugget = SlideshowSnugget.objects.create(**kwargs)
  snugget.pop_out = addPopOutIfExists(row)
  addSlideshow(os.path.join(dataDir, 'images/', row["image_slideshow_folder"]), snugget)
  snugget.save()


def addSlideshow(folder, snugget):
  slideshowFile = os.path.join(folder, "slideshow.csv")

  with open(slideshowFile) as csvFile:
    slides = csv.DictReader(csvFile)
    rowCount = 1 # row 1 consists of field names, so row 2 is the first data row. We'll increment this before first referencing it.
    for row in slides:
      rowCount += 1
      photo = PastEventsPhoto.objects.create(group=snugget, caption=row["caption"])
      if row["image"] != '':
        imageFile = os.path.join(folder, row["image"])
        with open(imageFile, 'rb') as f:
          data = File(f)
          photo.image.save(row["image"], data, True)
      print("Created", photo)

  print("Image slideshow created from", folder)


def findAllFilterVals(shapefile):
  fieldName = getFilterFieldName(shapefile)
  return shapefile.objects.values_list(fieldName, flat=True)


def checkForSnugget(shapefile, section, filterColumn, filterVal):
  kwargs = {'section': section, filterColumn: getShapefileFilter(shapefile, filterVal)}
  if Snugget.objects.filter(**kwargs).exists():
    return Snugget.objects.select_subclasses().get(**kwargs)
  else:
    return None


def removeOldSnugget(shapefile, section, filterColumn, filterVal):
  kwargs = {'section': section, filterColumn: getShapefileFilter(shapefile, filterVal)}
  Snugget.objects.filter(**kwargs).delete()


# Check with the user about overwriting existing snuggets, giving them the options to:
# either quit and check what's going on, or say "yes to all" and not get prompted again.
def askUserAboutOverwriting(row, old, overwriteAll):
  if overwriteAll: # if it's already set, then don't do anything else
    return True
  else:
    if old is not None and not isinstance(old, list):
      print("In shapefile ", repr(row["shapefile"]), " there is already a snugget defined for section " , repr(row["section"]), ", intensity ", repr(row["lookup_value"]), " with the following text content:", sep="")
      print(old)
    elif isinstance(old, list):
      print("In shapefile ", repr(row["shapefile"]), " there are existing snuggets for section" , repr(row["section"]), " with the following text content:", sep="")
      for snugget in old:
        print(snugget)
    else:
      # if no existing snuggets were found, then we neither need to ask the user this time nor change overwriteAll
      return overwriteAll

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
