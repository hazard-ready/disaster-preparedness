import os
import subprocess

import shapefile

def main():
  desiredSRID = "4326"  # EPSG:4326 = Google Mercator
  SRIDNamespace = "EPSG"
  simplificationTolerance = "0.00001"  # This is in the SRS's units. For EPSG:4326, that's decimal degrees

  appDir = "disasterinfosite"
  dataDir = os.path.join(appDir, "data")
  reprojectedDir = os.path.join(dataDir, "reprojected")
  simplifiedDir = os.path.join(dataDir, "simplified")
  modelsFile = os.path.join(appDir, "models.py")
  adminFile = os.path.join(appDir, "admin.py")
  loadFile = os.path.join(appDir, "load.py")
  viewsFile = os.path.join(appDir, "views.py")

  existingShapefileGroups = []

  modelsLocationsList = ""
  modelsClasses = ""
  modelsFilters = ""
  modelsGeoFilters = ""
  modelsSnuggetRatings = ""
  adminModelImports = "from .models import EmbedSnugget, TextSnugget, SnuggetSection, SnuggetSubSection, Location, SiteSettings, SupplyKit, ImportantLink"
  adminFilterRefs = ""
  adminSiteRegistrations = ""
  loadMappings = ""
  loadPaths = ""
  loadImports = ""
  loadGroups = "    from .models import ShapefileGroup\n"
  viewsSnuggetMatches = ""
  templateMomentSnuggets = ""

  for subdir in [reprojectedDir, simplifiedDir]:
    if not os.path.exists(subdir):
      os.mkdir(subdir)

  first = True
  for f in os.listdir(dataDir):
    if f[-4:].lower() == ".shp":
      stem = f[:-4].replace(".", "_").replace("-","_")
      print("Opening shapefile:", stem)
      #TODO: if there's already a reprojected shapefile, use the field in that instead of prompting the user.
      sf = shapefile.Reader(os.path.join(dataDir, f))
      keyField = askUserForFieldNames(sf, stem)
      shapefileGroup = askUserForShapefileGroup(stem, existingShapefileGroups)

      reprojected = processShapefile(f, stem, dataDir, reprojectedDir, SRIDNamespace+":"+desiredSRID, keyField)
      simplified = simplifyShapefile(reprojected, simplifiedDir, simplificationTolerance)
      sf = shapefile.Reader(simplified)
      shapeType = detectGeometryType(sf, stem)
      encoding = findEncoding(sf, dataDir, stem)

#Code generation: one line in this function writes one line of code to be copied elsewhere
# one block represents the code generation for each destination file
      modelsLocationsList += "            '" + stem + "': " + stem + ".objects.data_bounds(),\n"

      modelsClasses += modelClassGen(stem, sf, keyField, desiredSRID, shapeType, shapefileGroup)
      modelsFilters += "    " + stem + "_filter = models.ForeignKey(" + stem + ", related_name='+', on_delete=models.PROTECT, blank=True, null=True)\n"
      modelsGeoFilters += modelsGeoFilterGen(stem, keyField)
      if shapefileGroup not in existingShapefileGroups:
        existingShapefileGroups.append(shapefileGroup)
        loadGroups += "    " + shapefileGroup + " = ShapefileGroup.objects.get_or_create(name='" + shapefileGroup + "')\n"
      modelsSnuggetRatings += "                '" + stem + "_rating': " + stem + "_rating,\n"

      adminModelImports += ", " + stem
      if not first:
        adminFilterRefs += ", "
      adminFilterRefs += "'" + stem + "_filter'"
      adminSiteRegistrations += "admin.site.register(" + stem + ", GeoNoEditAdmin)\n"

      loadMappings += stem + "_mapping = {\n"
      loadMappings += "    '" + keyField.lower() + "': '" + keyField + "',\n"
      loadMappings += "    'geom': '" + shapeType.upper() + "'\n"
      loadMappings += "}\n\n"
      loadPaths += stem + "_shp = " + "os.path.abspath(os.path.join(os.path.dirname(__file__)," + " '../" + simplified + "'))\n"
      loadImports += "    from .models import " + stem + "\n"
      loadImports += "    lm_" + stem + " = LayerMapping(" + stem + ", " + stem + "_shp, " + stem + "_mapping, transform=True, " + "encoding='" + encoding + "', unique=['" + keyField.lower() + "'])\n"
      loadImports += "    lm_" + stem + ".save(strict=True, verbose=verbose)\n\n"

      print("")
      first = False

  # clear trailing comma from this one
  modelsLocationsList = modelsLocationsList.strip(",\n") + "\n"

  # assemble the whole return statement for the snugget class after going through the loop
  modelsSnuggetReturns = "        return {'groups': groupsDict,\n"
  modelsSnuggetReturns += modelsSnuggetRatings.strip(",\n") + "\n"
  modelsSnuggetReturns += "                }\n"

  # make sure this gets its own line of code
  adminModelImports += "\n"

  # assembling the complete lists for the start of class SnuggetAdmin in admin.py
  adminLists  = "    list_display = ('shortname', 'section', 'sub_section', " + adminFilterRefs + ")\n"
  adminLists += "    list_filter = ('section', 'sub_section', " + adminFilterRefs + ")\n\n"
  adminLists += "    fieldsets = (\n"
  adminLists += "        (None, {\n"
  adminLists += "            'fields': ('section', 'sub_section')\n"
  adminLists += "        }),\n"
  adminLists += "        ('Filters', {\n"
  adminLists += "            'description': 'Choose a filter value this snugget will show up for.  It is recommended you only select a value for one filter and leave the rest empty.',\n"
  adminLists += "            'fields': ((" + adminFilterRefs + "))\n"
  adminLists += "        })\n"
  adminLists += "    )\n"

  outputGeneratedCode(modelsLocationsList, modelsFile, "locationsList")
  outputGeneratedCode(modelsClasses, modelsFile, "modelsClasses")
  outputGeneratedCode(modelsFilters, modelsFile, "modelsFilters")
  outputGeneratedCode(modelsGeoFilters + "\n" + modelsSnuggetReturns, modelsFile, "modelsGeoFilters")

  outputGeneratedCode(adminModelImports, adminFile, "adminModelImports")
  outputGeneratedCode(adminLists, adminFile, "adminLists")
  outputGeneratedCode(adminSiteRegistrations, adminFile, "adminSiteRegistrations")

  outputGeneratedCode(loadMappings + "\n" + loadPaths, loadFile, "loadMappings")
  outputGeneratedCode(loadGroups, loadFile, "loadGroups")
  outputGeneratedCode(loadImports, loadFile, "loadImports")

  print("\n")




def sanitiseInput(inputString):
  '''
  Character replacement algorithm from http://stackoverflow.com/a/27086669/2121470
  I chose the fastest of the solutions I found easily legible.
  The reason for anticipating so many variants of dashes and quotes is that MS Word can insert many of these without the user intending them.
  '''
  for char in ['\\', '`', '*', ' ', '{', '}', '[', ']', '(', ')', '>', '<', '#', '№', '+', '-', '‐', '‒', '–', '—', '.', '¡', '!', '$', '\'', ',', '"', '/', '%', '‰', '‱', '‘', '’', '“', '”', '&', '@', '¿', '?', '~', '^', '=', ';', ':', '|']:
    if char in inputString:
      inputString = inputString.replace(char, '_')

  return inputString




"""
processShapefile() makes two changes in one shot:
* Reprojects the shapefile to srs, because geoDjango has issues if they're not all in the same SRS
* Dissolves shapes on keyField so that we'll end up with one database row per unique keyField value
Simplifying the shapefile is done by a separate function, because the units for simplification tolerance
depend on the spatial representation system being used, and can't even be straightforwardly converted (since degrees
to metres depends on the latitude). The simplest way to simplify with a uniform tolerance is to do it after
standardising the SRS.
"""
def processShapefile(f, stem, inputDir, outputDir, srs, keyField):
  original = os.path.join(inputDir, f)
  reprojected = os.path.join(outputDir, f)
  if os.path.exists(reprojected):
    print("Skipping reprojection because this file has previously been reprojected.")
  else:
    print("Aggregating shapes with the same value of", keyField, "and reprojecting to", srs)
    sqlCmd = 'select ST_Union(Geometry),' + keyField + ' from ' + stem + ' GROUP BY ' + keyField
    ogrCmd = [
      "ogr2ogr",
      reprojected,
      original,
      "-dialect", "sqlite", "-sql", sqlCmd,
      "-t_srs", srs
    ]
    subprocess.call(ogrCmd)
  return reprojected




def simplifyShapefile(original, outputDir, tolerance):
  simplified = os.path.join(outputDir, os.path.basename(original))
  if os.path.exists(simplified):
    print("Skipping simplification because this file has previously been simplified.")
  else:
    print("Simplifying with tolerance", tolerance)
    ogrCmd = [
      "ogr2ogr",
      simplified,
      original,
      "-simplify", tolerance
    ]
    subprocess.call(ogrCmd)
    print(original, "simplified.")
  return simplified



def askUserForFieldNames(sf, stem):
  fieldNames = [x[0] for x in sf.fields[1:]]
  print("Found the following fields in the attribute table:")
  print(str(fieldNames).strip("[]").replace("'",""))
  print("Which would you like to use to look up snuggets by?")
  keyField = False
  while keyField not in fieldNames:
    keyField = input(">> ")
  print("Generating code for", stem, "using", keyField, "to look up snuggets.")
  return keyField



def askUserForShapefileGroup(stem, existingShapefileGroups):
  if existingShapefileGroups != []:
    print("So far, you have defined the following shapefile groups:")
    print((str(existingShapefileGroups).strip("[]").replace("'","")))
  print("If you would like to group", stem, "in a tab with content from other shapefiles, type a group name here:")
  print("(Leave blank to give content from this shapefile its own unique tab.)")
  groupName = input(">> ")
  groupName = sanitiseInput(groupName)
  # Doing the above replacement here is somewhat wasteful, but it means that the user will consistently see the sanitised group name echoed back to them in prompts.

  if groupName in existingShapefileGroups:
    print("Adding", stem, "to group:", groupName)
  else:
    print("Creating new group", groupName, "and adding", stem, "to it.")

  if groupName == "":
    return stem
  else:
    return groupName



def detectGeometryType(sf, stem):
  try:
    shapeType = next(shape for shape in sf.shapes() if shape.shapeType != 0).shapeType
  except StopIteration:
    print("No valid geometries found in", stem, "- please check the shapefile")
    exit()
  if shapeType == 5 or shapeType == 15:
    return "MultiPolygon"
  elif shapeType == 3 or shapeType == 13:
    print("WARNING:", stem, "has a linear geometry, and this application currently only handles polygons properly")
    return "MultiLineString"
  elif shapeType == 1 or shapeType == 8 or shapeType == 11 or shapeType == 18:
    print("WARNING:", stem, "has a point geometry, and this application currently only handles polygons properly")
    return "MultiPoint"
  elif shapeType > 20:
  	print("Support for Multipart geometries is not implemented yet")
  	exit()
  else:
    print("Geometry field type ", shapeType, "unrecognised")
# the list of valid geometry field type codes is at
# https://www.esri.com/library/whitepapers/pdfs/shapefile.pdf p4
# but see also caveat at
# https://gis.stackexchange.com/questions/122816/shapefiles-polygon-type-is-it-in-fact-multipolygon
    exit()



def findEncoding(sf, inputDir, stem):
  encodingFile = os.path.join(inputDir, stem+".cpg")
# if .cpg is not found, try .CPG in case we're on a case sensitive file system
  if not os.path.exists(encodingFile):
  	encodingFile = os.path.join(inputDir, stem+".CPG")

  if os.path.exists(encodingFile):
    with open(encodingFile, 'r') as f:
      encoding = f.read()
    print("Determined that", stem, "uses character encoding", encoding)
# TODO: implement the chardet method from https://gist.github.com/jatorre/939830 as another option
  else:
    print("Unable to automatically detect the character encoding of", stem)
    print("What encoding should we use? (If unknown, try UTF-8)")
    encoding = input(">> ")
  return encoding



# See https://pypi.python.org/pypi/pyshp#reading-records for the array format
def findFieldType(sf, fieldName):
  for field in sf.fields:
    if field[0] == fieldName:
      if field[1] == 'C':
        return "CharField(max_length=" + str(field[2]) + ")"
      elif field[1] == 'N':
        if field[3] > 0:
          return "FloatField()"
        else:
          return "IntegerField()"
      else:
        print("Field type unrecognised:")
        print(field)
        exit()



def modelClassGen(stem, sf, keyField, srs, shapeType, shapefileGroup):
  text  = "class " + stem + "(models.Model):\n"
  text += "    def getGroup():\n"
  text += "        return ShapefileGroup.objects.get_or_create(name='" + shapefileGroup + "')[0].id\n\n"
  text += "    " + keyField.lower() + " = models." + findFieldType(sf, keyField) + "\n"
  text += "    geom = models." + shapeType + "Field(srid=" + srs + ")\n"
  text += "    objects = ShapeManager()\n\n"
  text += "    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)\n"
  text += "    def __str__(self):\n"
  text += "        return str(self." + keyField.lower() + ")\n\n"

  return text



def modelsGeoFilterGen(stem, keyField):
  text  = "        qs_" + stem + " = " + stem + ".objects.filter(geom__contains=pnt)\n"
  text += "        " + stem + "_rating = " + "qs_" + stem + ".values_list('" + keyField.lower() + "', flat=True)\n"
  text += "        for rating in " + stem + "_rating:\n"
  text += "            individualSnugget = Snugget.objects.filter(" + stem + "_filter__" + keyField.lower() + "__exact=rating).select_subclasses()\n"
  text += "            if individualSnugget:\n"
  text += "                groupsDict[individualSnugget[0].group.name].extend(individualSnugget)\n\n"
  return text



def outputGeneratedCode(code, destFile, anchor):
  linesWanted = True
  insertComplete = False
  tempFile = destFile + ".tmp"
  with open(destFile, 'r') as f_in:
    with open (tempFile, 'w') as f_out:
      for line in f_in:
        if not linesWanted:
          if ("# END OF GENERATED CODE BLOCK") in line:
            linesWanted = True
            insertComplete = True
        if linesWanted:
          f_out.write(line)
        if ("# " + anchor) in line:
          linesWanted = False
          f_out.write(code)

  if insertComplete:
    os.remove(destFile)
    os.rename(tempFile, destFile)
    print(anchor, "code written to", destFile)
  else:
    print(anchor, "not found in", destFile)



if __name__ == "__main__":
  main()
