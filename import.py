import os
import subprocess
import sys

from django.contrib.gis.utils.ogrinspect import ogrinspect
import shapefile

def main():
  dataDir = "world/data"
  reprojectedDir = os.path.join(dataDir, "reprojected")
  simplifiedDir = os.path.join(dataDir, "simplified")

  modelsClasses = ""
  modelsFilters = ""
  modelsGeoFilters = ""
  adminModelImports = "from .models import TextSnugget, EmbedSnugget, SnuggetSection, SnuggetSubSection, Infrastructure, InfrastructureGroup, InfrastructureCategory, RecoveryLevels, Location, SiteSettings"
#  adminSiteRegistrations = ""
  modelsSnuggetReturns = ""
  viewsSnuggetMatches = ""
  adminLists = ""
  loadMappings = ""
  loadPaths = ""
  templateMomentSnuggets = ""
  loadImports = ""

  for subdir in [reprojectedDir, simplifiedDir]:
    if not os.path.exists(subdir):
      os.mkdir(subdir)

  for f in os.listdir(dataDir):
    if f[-4:] == ".shp":
      stem = f[:-4].replace(".", "_").replace("-","_")
      print("Opening shapefile:", stem)
      reprojected = reprojectShapefile(f, dataDir, reprojectedDir, "EPSG:4326")
      simplified = simplifyShapefile(reprojected, simplifiedDir, "0.0001")
      sf = shapefile.Reader(simplified)
      fieldNames = [x[0] for x in sf.fields[1:]]
      print("Found the following fields in the attribute table:")
      print(str(fieldNames).strip("[").strip("]").replace("'",""))
      print("Which would you like to use to look up snuggets by?")
      keyField = False
      while keyField not in fieldNames:
        keyField = input()

# TODO: figure out if there's any problem caused by implicitly converting non-multi geometries to multi-types; if so, decide how to handle that
      modelsClasses += ogrinspect(simplified, stem, srid=4326, multi_geom=True) + "\n\n\n"
      modelsFilters += stem + "_filter = models.ForeignKey(" + stem
      modelsFilters += ", related_name='+', on_delete=models.PROTECT, blank=True, null=True)\n"
      modelsGeoFilters += "qs_" + stem + " = " + stem + ".objects.filter(geom__contains=pnt)\n"

      adminModelImports += ", " + stem

      print("")

  # no need to keep repeating the import statement that ogrinspect puts in
  modelsClasses = modelsClasses.replace("from django.contrib.gis.db import models\n\n", "")

  outputGeneratedCode(modelsClasses, "world/models.py", "Insert generated modelsClasses here")
  outputGeneratedCode(modelsFilters, "world/models.py", "Insert generated modelsFilters here")
  outputGeneratedCode(modelsGeoFilters, "world/models.py", "Insert generated modelsGeoFilters here")
  outputGeneratedCode(adminModelImports, "world/admin.py", "Replace the next line with generated adminModelImports", replace=True)



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
      "-t_srs", "EPSG:4326"
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
  return simplified



def outputGeneratedCode(code, destFile, anchor, replace=False):
  print("\n######################################################\n\n\n\n")
  if replace:
  	prompt = "Replace the line after the '" + anchor + "' comment in "
  	prompt += destFile + " with the following code:\n"
  else:
  	prompt = "Insert the following code after the '" + anchor + "' comment in "
  	prompt += destFile + "\n\n"
  print(prompt)
  print(code)



if __name__ == "__main__":
  main()
