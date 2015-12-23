import os
import subprocess
import sys

# from django.contrib.gis.utils.ogrinspect import ogrinspect
import shapefile

def main():
  desiredSRID = "4326"
  SRIDNamespace = "EPSG"
  simplificationTolerance = "0.0001"

  dataDir = "world/data"
  reprojectedDir = os.path.join(dataDir, "reprojected")
  simplifiedDir = os.path.join(dataDir, "simplified")

  modelsClasses = ""
  modelsFilters = ""
  modelsGeoFilters = ""
  modelsSnuggetGroups = ""
  modelsSnuggetRatings = ""
  adminModelImports = "from .models import TextSnugget, EmbedSnugget, SnuggetSection, SnuggetSubSection, RecoveryLevels, Location, SiteSettings"
# taking infrastructure refs out for now; they may not be worth automating in the same way
#  adminModelImports = "from .models import TextSnugget, EmbedSnugget, SnuggetSection, SnuggetSubSection, Infrastructure, InfrastructureGroup, InfrastructureCategory, RecoveryLevels, Location, SiteSettings"
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

  i = 0
  for f in os.listdir(dataDir):
    if f[-4:] == ".shp":
      stem = f[:-4].replace(".", "_").replace("-","_")
      print("Opening shapefile:", stem)
      reprojected = reprojectShapefile(f, dataDir, reprojectedDir, SRIDNamespace+":"+desiredSRID)
      simplified = simplifyShapefile(reprojected, simplifiedDir, simplificationTolerance)
      sf = shapefile.Reader(simplified)

      keyField, uniqueField = askUserForFieldNames(sf, stem)
      shapeType = detectGeometryType(sf, stem)
      encoding = findEncoding(sf, dataDir, stem)

      modelsClasses += modelClassGen(stem, sf, keyField, uniqueField, desiredSRID, shapeType)
      modelsFilters += "    " + stem + "_filter = models.ForeignKey(" + stem
      modelsFilters += ", related_name='+', on_delete=models.PROTECT, blank=True, null=True)\n"
      modelsGeoFilters += modelsGeoFilterGen(stem, keyField)
      modelsSnuggetGroups += "                          '"
      modelsSnuggetGroups += stem + "_snugs': " + stem + "_snuggets,\n"
      modelsSnuggetRatings += "                '"
      modelsSnuggetRatings += stem + "_rating': " + stem + "_rating,\n"

      adminModelImports += ", " + stem
      if i > 0:
        adminFilterRefs += ", "
      adminFilterRefs += "'" + stem + "_filter'"
      adminSiteRegistrations += "admin.site.register(" + stem
      adminSiteRegistrations += ", GeoNoEditAdmin)\n"

      loadMappings += stem + "_mapping = {\n"
      loadMappings += "    '" + keyField.lower() + "': '" + keyField + "',\n"
      if keyField != uniqueField:
        loadMappings += "    '" + uniqueField.lower() + "': '" + uniqueField + "',\n"
      loadMappings += "    'geom': '" + shapeType.upper() + "'\n"
      loadMappings += "}\n\n"
      loadPaths += stem + "_shp = " + "os.path.abspath(os.path.join(os.path.dirname(__file__),"
      loadPaths += " '../" + simplified + "'))\n"
      loadImports += "    from .models import " + stem + "\n"
      loadImports += "    lm_" + stem + " = LayerMapping(" + stem + ", "
      loadImports += stem + "_shp, " + stem + "_mapping, transform=True, "
      loadImports += "encoding='" + encoding
      loadImports += "', unique=['" + uniqueField.lower() + "'])\n"
      loadImports += "    lm_" + stem + ".save(strict=True, verbose=verbose)\n\n"

      viewsSnuggetMatches += "            if snugget_content['structured']['moment']['"
      viewsSnuggetMatches += stem + "_snugs']:\n"
      viewsSnuggetMatches += "                wrapper_width += base_section_width\n"
      viewsSnuggetMatches += "                n_sections += 1\n"

      print("")
      i = i + 1

  # no need to keep repeating the import statement that ogrinspect puts in
  modelsClasses = modelsClasses.replace("from django.contrib.gis.db import models\n\n", "")

  # assemble the whole return statement for the snugget class after going through the loop
  modelsSnuggetReturns = "        return {'groups': {\n"
  modelsSnuggetReturns += modelsSnuggetGroups.strip("\n").strip(",")
  modelsSnuggetReturns += "\n                          },\n"
  modelsSnuggetReturns += modelsSnuggetRatings.strip("\n").strip(",")
  modelsSnuggetReturns += "\n                }"

  # assembling the complete lists for the start of class SnuggetAdmin in admin.py
  adminLists = "    list_display = ('shortname', 'section', 'sub_section', "
  adminLists += adminFilterRefs + ")\n"
  adminLists += "    list_filter = ('section', 'sub_section', "
  adminLists += adminFilterRefs + ")\n\n"
  adminLists += "    fieldsets = (\n"
  adminLists += "        (None, {\n"
  adminLists += "            'fields': ('section', 'sub_section')\n"
  adminLists += "        }),\n"
  adminLists += "        ('Filters', {\n"
  adminLists += "            'description': 'Choose a filter value this snugget will show up for.  It is recommended you only select a value for one filter and leave the rest empty.',\n"
  adminLists += "            'fields': ((" + adminFilterRefs + "))\n"
  adminLists += "        })\n"
  adminLists += "    )\n"
  outputGeneratedCode(modelsClasses, "world/models.py", "Insert generated modelsClasses here")
  outputGeneratedCode(modelsFilters, "world/models.py", "Insert generated modelsFilters here")
  outputGeneratedCode(modelsGeoFilters, "world/models.py", "Insert generated modelsGeoFilters here")
  outputGeneratedCode(modelsSnuggetReturns, "world/models.py", "Insert generated modelsSnuggetReturns here")

  outputGeneratedCode(adminModelImports, "world/admin.py", "Replace the next line with generated adminModelImports", replace=True)
  outputGeneratedCode(adminLists, "world/admin.py", "Insert generated adminLists here", replace=True)
  outputGeneratedCode(adminSiteRegistrations, "world/admin.py", "Insert generated adminSiteRegistrations here")

  outputGeneratedCode(loadMappings, "world/load.py", "Insert generated loadMappings here")
  outputGeneratedCode(loadPaths, "world/load.py", "Insert generated loadPaths here")
  outputGeneratedCode(loadImports, "world/load.py", "Insert generated loadImports here")

  outputGeneratedCode(viewsSnuggetMatches, "world/views.py", "Insert generated viewsSnuggetMatches here")

  print("\n")



def reprojectShapefile(f, inputDir, outputDir, srs):
  original = os.path.join(inputDir, f)
  reprojected = os.path.join(outputDir, f)
  if os.path.exists(reprojected):
    print("Skipping reprojection because this file has previously been reprojected.")
  else:
    print("Reprojecting to", srs)
    ogrCmd = [
      "ogr2ogr",
      reprojected,
      original,
      "-t_srs", srs
    ]
    subprocess.call(ogrCmd)
  return reprojected



def simplifyShapefile(original, outputDir, tolerance):
  simplified = os.path.join(outputDir, os.path.basename(original))
  if os.path.exists(simplified):
    print("Skipping simplification because this file has previously been reprojected.")
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
  print(str(fieldNames).strip("[").strip("]").replace("'",""))
  print("Which would you like to use to look up snuggets by?")
  keyField = False
  while keyField not in fieldNames:
    keyField = input(">> ")
#TODO: make sure it really is OK for key & unique fields to be the same
  print("Which is unique for each shape? (can be the same field as before)")
  uniqueField = False
  while uniqueField not in fieldNames:
    uniqueField = input(">> ")
  print("Generating code for", stem, "using the following fields:")
  print("'" + keyField + "' to look up snuggets.")
  print("'" + uniqueField + "' as the unique ID.")
  return keyField, uniqueField



def detectGeometryType(sf, stem):
  shapeType = 0
  i = 0
  while shapeType == 0:
    shapeType = sf.shapes()[i].shapeType
    i = i + 1
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



def modelClassGen(stem, sf, keyField, uniqueField, srs, shapeType):
  text = "class " + stem + "(models.Model):\n"
  text += "    " + keyField.lower() + " = models." + findFieldType(sf, keyField) + "\n"
  if uniqueField != keyField:
    text += "    " + uniqueField.lower() + " = models." + findFieldType(sf, uniqueField) + "\n"
  text += "    geom = models." + shapeType + "Field(srid=" + srs + ")\n"
  text += "    objects = models.GeoManager()\n\n"
  text += "    def __str__(self):\n"
  text += "        return str(self." + keyField.lower() + ")\n\n"

  return text



def modelsGeoFilterGen(stem, keyField):
  text = "        qs_" + stem + " = "
  text += stem + ".objects.filter(geom__contains=pnt)\n"
  text += "        " + stem + "_rating = "
  text += "qs_" + stem + ".values.list('" + keyField.lower() + "', flat=True)\n"
  text += "        " + stem + "_snuggets = "
  text += "Snugget.objects.filter(" + stem + "_filter__" + keyField.lower() + "__exact="
  text += stem + "_rating).select_subclasses()\n\n"
  return text



def outputGeneratedCode(code, destFile, anchor, replace=False):
  print("\n######################################################\n")
  if replace:
  	prompt = "Replace the line[s] after the '" + anchor + "' comment in "
  	prompt += destFile + " with the following code:\n"
  else:
  	prompt = "Insert the following code after the '" + anchor + "' comment in "
  	prompt += destFile + "\n\n"
  print(prompt)
  print(code)



if __name__ == "__main__":
  main()
