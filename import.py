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
  adminModelImports = "from .models import TextSnugget, EmbedSnugget, SnuggetSection, SnuggetSubSection, Infrastructure, InfrastructureGroup, InfrastructureCategory, RecoveryLevels, Location, SiteSettings"
  adminListDisplay = "    list_display = ('shortname', 'section', 'sub_section'"
  adminListFilter = "    list_filter = ('section', 'sub_section'"
  adminSiteRegistrations = ""
  loadMappings = ""
  loadPaths = ""
  viewsSnuggetMatches = ""
  templateMomentSnuggets = ""
  loadImports = ""

  for subdir in [reprojectedDir, simplifiedDir]:
    if not os.path.exists(subdir):
      os.mkdir(subdir)

  for f in os.listdir(dataDir):
    if f[-4:] == ".shp":
      stem = f[:-4].replace(".", "_").replace("-","_")
      print("Opening shapefile:", stem)
      reprojected = reprojectShapefile(f, dataDir, reprojectedDir, SRIDNamespace+":"+desiredSRID)
      simplified = simplifyShapefile(reprojected, simplifiedDir, simplificationTolerance)
      sf = shapefile.Reader(simplified)

      keyField = askUserForKeyField(sf, stem)
      shapeType = detectGeometryType(sf, stem)

      modelsClasses += modelClassGen(stem, sf, keyField, desiredSRID, shapeType)
      modelsFilters += "    " + stem + "_filter = models.ForeignKey(" + stem
      modelsFilters += ", related_name='+', on_delete=models.PROTECT, blank=True, null=True)\n"
      modelsGeoFilters += modelsGeoFilterGen(stem, keyField)
      modelsSnuggetGroups += "                          '"
      modelsSnuggetGroups += stem + "_snugs': " + stem + "_snuggets,\n"
      modelsSnuggetRatings += "                '"
      modelsSnuggetRatings += stem + "_rating': " + stem + "_rating,\n"

      adminModelImports += ", " + stem
      adminListDisplay += ", '" + stem + "_filter'"
      adminListFilter += ", '" + stem + "_filter'"
      adminSiteRegistrations += "admin.site.register(" + stem
      adminSiteRegistrations += ", GeoNoEditAdmin)\n"

      viewsSnuggetMatches += "            if snugget_content['structured']['moment']['"
      viewsSnuggetMatches += stem + "_snugs']:\n"
      viewsSnuggetMatches += "                wrapper_width += base_section_width\n"
      viewsSnuggetMatches += "                n_sections += 1\n"

      print("")

  # no need to keep repeating the import statement that ogrinspect puts in
  modelsClasses = modelsClasses.replace("from django.contrib.gis.db import models\n\n", "")

  # assemble the whole return statement for the snugget class after going through the loop
  modelsSnuggetReturns = "        return {'groups': {\n"
  modelsSnuggetReturns += modelsSnuggetGroups.strip("\n").strip(",")
  modelsSnuggetReturns += "\n                          },\n"
  modelsSnuggetReturns += modelsSnuggetRatings.strip("\n").strip(",")
  modelsSnuggetReturns += "\n                }"

  # assembling the complete lists for the start of class SnuggetAdmin in admin.py
  adminLists = adminListDisplay + ")\n" + adminListFilter + ")\n"

  outputGeneratedCode(modelsClasses, "world/models.py", "Insert generated modelsClasses here")
  outputGeneratedCode(modelsFilters, "world/models.py", "Insert generated modelsFilters here")
  outputGeneratedCode(modelsGeoFilters, "world/models.py", "Insert generated modelsGeoFilters here")
  outputGeneratedCode(modelsSnuggetReturns, "world/models.py", "Insert generated modelsSnuggetReturns here")

  outputGeneratedCode(adminModelImports, "world/admin.py", "Replace the next line with generated adminModelImports", replace=True)
  outputGeneratedCode(adminLists, "world/admin.py", "Insert generated adminLists here", replace=True)
  outputGeneratedCode(adminSiteRegistrations, "world/models.py", "Insert generated adminSiteRegistrations here")

  outputGeneratedCode(viewsSnuggetMatches, "world/models.py", "Insert generated viewsSnuggetMatches here")
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



def askUserForKeyField(sf, stem):
  fieldNames = [x[0] for x in sf.fields[1:]]
  print("Found the following fields in the attribute table:")
  print(str(fieldNames).strip("[").strip("]").replace("'",""))
  print("Which would you like to use to look up snuggets by?")
  keyField = False
  while keyField not in fieldNames:
    keyField = input(">> ")
  print("Generating code for", stem, "using field", keyField, "to look up snuggets.")
  return keyField



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
  	return "PolyLine"
  else:
  	print("Geometry field type ", shapeType, "unrecognised")
  	# the list of valid geometry field type codes is at
  	# https://www.esri.com/library/whitepapers/pdfs/shapefile.pdf p4
  	# but see also caveat at
  	# https://gis.stackexchange.com/questions/122816/shapefiles-polygon-type-is-it-in-fact-multipolygon
  	exit()



def modelClassGen(stem, sf, keyField, srs, shapeType):
  text = "class " + stem + "(models.Model):\n"
  text += "    " + keyField + " = models."
  for field in sf.fields:
    if field[0] == keyField:
      if field[1] == 'C':
        text += "CharField(max_length=" + str(field[2]) + ")\n"
      elif field[1] == 'N':
        if field[3] > 0:
          text += "FloatField()\n"
        else:
          text += "IntegerField()\n"
      else:
        print("Field type unrecognised:")
        print(field)
        exit()
  text += "    geom = models." + shapeType + "Field(srid=" + srs + ")\n"
  text += "    objects = models.GeoManager()\n\n"
  text += "    def __str__(self):\n"
  text += "        return self." + keyField + "\n\n"

  return text



def modelsGeoFilterGen(stem, keyField):
  text = "        qs_" + stem + " = "
  text += stem + ".objects.filter(geom__contains=pnt)\n"
  text += "        " + stem + "_rating = "
  text += "qs_" + stem + ".values.list('" + keyField + "', flat=True)\n"
  text += "        " + stem + "_snuggets = "
  text += "Snugget.objects.filter(" + stem + "_filter__" + keyField + "__exact="
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
