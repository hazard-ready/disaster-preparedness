import os
import subprocess
import sys

from django.contrib.gis.utils.ogrinspect import ogrinspect

def main():
  dataDir = "world/data"
  reprojectedDir = os.path.join(dataDir, "reprojected")
  simplifiedDir = os.path.join(dataDir, "simplified")

  modelsClasses = ""
  adminModelImports = "from .models import TextSnugget, EmbedSnugget, SnuggetSection, SnuggetSubSection, Infrastructure, InfrastructureGroup, InfrastructureCategory, RecoveryLevels, Location, SiteSettings"
  adminSiteRegistrations = ""
  modelsFilters = ""
  modelsGeoFilters = ""
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
      modelsClasses += ogrinspect(simplified, stem, srid=4326) + "\n\n\n"
      adminModelImports += ", " + stem

      print("")

  # no need to keep repeating the import statement that ogrinspect puts in
  modelsClasses = modelsClasses.replace("from django.contrib.gis.db import models\n\n", "")
  outputGeneratedCode(modelsClasses, "world/models.py", "Insert generated modelsClasses here")
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
  	prompt = "Replace the '" + anchor + "' comment in " + destFile
  	prompt += " with the following code:\n\n"
  else:
  	prompt = "Insert the following code after the '" + anchor + "' comment in "
  	prompt += destFile + "\n\n"
  print(prompt)
  print(code)



if __name__ == "__main__":
  main()
