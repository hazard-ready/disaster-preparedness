import os
import subprocess

import shapefile

def main():
  desiredSRID = "4326"  # EPSG:4326 = Google Mercator
  SRIDNamespace = "EPSG"
  simplificationTolerance = "0.00001"  # This is in the SRS's units. For EPSG:4326, that's decimal degrees

  appDir = "world"
  dataDir = os.path.join(appDir, "data")
  reprojectedDir = os.path.join(dataDir, "reprojected")
  simplifiedDir = os.path.join(dataDir, "simplified")
  modelsFile = os.path.join(appDir, "models.py")
  adminFile = os.path.join(appDir, "admin.py")
  loadFile = os.path.join(appDir, "load.py")
  viewsFile = os.path.join(appDir, "views.py")

  modelsClasses = ""
  modelsFilters = ""
  modelsGeoFilters = ""
  modelsSnuggetGroups = ""
  modelsSnuggetRatings = ""
  adminModelImports = "from .models import TextSnugget, EmbedSnugget, SnuggetSection, SnuggetSubSection, RecoveryLevels, Location, SiteSettings"
  adminFilterRefs = ""
  adminSiteRegistrations = ""
  loadMappings = ""
  loadPaths = ""
  loadImports = ""
  viewsSnuggetMatches = ""
  templateMomentSnuggets = ""

  for subdir in [reprojectedDir, simplifiedDir]:
    if not os.path.exists(subdir):
      os.mkdir(subdir)

  first = True
  for f in os.listdir(dataDir):
    if f[-4:] == ".shp":
      stem = f[:-4].replace(".", "_").replace("-","_")
      print("Opening shapefile:", stem)
      #TODO: if there's already a reprojected shapefile, use the field in that instead of prompting the user.
      sf = shapefile.Reader(os.path.join(dataDir, f))
      keyField = askUserForFieldNames(sf, stem)

      reprojected = processShapefile(f, stem, dataDir, reprojectedDir, SRIDNamespace+":"+desiredSRID, keyField)
      simplified = simplifyShapefile(reprojected, simplifiedDir, simplificationTolerance)
      sf = shapefile.Reader(simplified)
      shapeType = detectGeometryType(sf, stem)
      encoding = findEncoding(sf, dataDir, stem)

#Code generation: one line in this function writes one line of code to be copied elsewhere
# one block represents the code generation for each destination file
      modelsClasses += modelClassGen(stem, sf, keyField, desiredSRID, shapeType)
      modelsFilters += "    " + stem + "_filter = models.ForeignKey(" + stem + ", related_name='+', on_delete=models.PROTECT, blank=True, null=True)\n"
      modelsGeoFilters += modelsGeoFilterGen(stem, keyField)
      modelsSnuggetGroups += "                          '" + stem + "_snugs': " + stem + "_snuggets,\n"
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

  # assemble the whole return statement for the snugget class after going through the loop
  modelsSnuggetReturns = "        return {'groups': {\n"
  modelsSnuggetReturns += modelsSnuggetGroups.strip(",\n") + "\n"
  modelsSnuggetReturns += "                          },\n"
  modelsSnuggetReturns += modelsSnuggetRatings.strip(",\n") + "\n"
  modelsSnuggetReturns += "                }\n"

  # make sure this gets its own line of code
  adminModelImports += "\n"
  
  # assembling the complete lists for the start of class SnuggetAdmin in admin.py
  adminLists = "    list_display = ('shortname', 'section', 'sub_section', " + adminFilterRefs + ")\n"
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

  outputGeneratedCode(modelsClasses, modelsFile, "modelsClasses")
  outputGeneratedCode(modelsFilters, modelsFile, "modelsFilters")
  outputGeneratedCode(modelsGeoFilters + "\n" + modelsSnuggetReturns, modelsFile, "modelsGeoFilters")

  outputGeneratedCode(adminModelImports, adminFile, "adminModelImports")
  outputGeneratedCode(adminLists, adminFile, "adminLists")
  outputGeneratedCode(adminSiteRegistrations, adminFile, "adminSiteRegistrations")

  outputGeneratedCode(loadMappings + "\n" + loadPaths, loadFile, "loadMappings")
  outputGeneratedCode(loadImports, loadFile, "loadImports")

  print("\n")



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
    print(ogrCmd)
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



def detectGeometryType(sf, stem):
  try:
    shapeType = next(shape for shape in sf.shapes() if shape.shapeType != 0).shapeType
  except stopIteration:
    print("No valid geometries found in", stem, "- please check the shapefile")
    exit()
  if shapeType == 5:
    return "MultiPolygon"
  elif shapeType == 3:
    print("WARNING:", stem, "has a linear geometry, and this application currently only handles polygons properly")
    return "MultiLineString"
  else:
    print("Geometry field type ", shapeType, "unrecognised")
# the list of valid geometry field type codes is at
# https://www.esri.com/library/whitepapers/pdfs/shapefile.pdf p4
# but see also caveat at
# https://gis.stackexchange.com/questions/122816/shapefiles-polygon-type-is-it-in-fact-multipolygon
    exit()



def findEncoding(sf, inputDir, stem):
  encodingFile = os.path.join(inputDir, stem+".cpg")
  if os.path.exists(encodingFile):
    with open(encodingFile, 'r') as f:
      encoding = f.read()
    print("Determined that", stem, "uses character encoding", encoding)
# TODO: implement the chardet method from https://gist.github.com/jatorre/939830 as another option
  else:
    print("Unable to automatically detect the character encoding of", stem)
    print("What encoding should we use? (If in doubt, choose UTF-8)")
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



def modelClassGen(stem, sf, keyField, srs, shapeType):
  text = "class " + stem + "(models.Model):\n"
  text += "    " + keyField.lower() + " = models." + findFieldType(sf, keyField) + "\n"
  text += "    geom = models." + shapeType + "Field(srid=" + srs + ")\n"
  text += "    objects = models.GeoManager()\n\n"
  text += "    def __str__(self):\n"
  text += "        return str(self." + keyField.lower() + ")\n\n"

  return text



def modelsGeoFilterGen(stem, keyField):
  text = "        qs_" + stem + " = " + stem + ".objects.filter(geom__contains=pnt)\n"
  text += "        " + stem + "_rating = " + "qs_" + stem + ".values_list('" + keyField.lower() + "', flat=True)\n"
  text += "        " + stem + "_snuggets = " + "Snugget.objects.filter(" + stem + "_filter__" + keyField.lower() + "__exact=" + stem + "_rating).select_subclasses()\n\n"
  return text



def outputGeneratedCode(code, destFile, anchor):
  startFound = False
  endFound = False
  tempFile = destFile + ".tmp"
  with open(destFile, 'r') as f_in:
    with open (tempFile, 'w') as f_out:
      for line in f_in:
        if startFound:
          if ("# END OF GENERATED CODE BLOCK") in line:
            endFound = True
        if (not startFound) or endFound:
          f_out.write(line)
        if ("# " + anchor) in line:
          startFound = True
          f_out.write(code) 
            
  if endFound:
    os.remove(destFile)
    os.rename(tempFile, destFile)
    print(anchor, "code written to", destFile)
  else:
    print(anchor, "not found in", destFile)

  
  
if __name__ == "__main__":
  main()
