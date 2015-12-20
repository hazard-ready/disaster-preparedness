import os
import subprocess
import sys

def main():
  workingDir = "world/data"
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
  for f in os.listdir(workingDir):
    if f[-4:] == ".shp" and f[-16:] != "_reprojected.shp":
      print("Opening shapefile:", f[:-4])
#TODO: simplify shapefile before or at the same time as reprojecting it?
      reprojected = reprojectShapefile(f, workingDir, "EPSG:4326")
      

      
def reprojectShapefile(f, workingDir, srs):
  reprojected = f[:-4] + "_reprojected.shp"
  if reprojected in os.listdir(workingDir):
    print("Skipping reprojection because this file has previously been reprojected.")
  else:
    print("Reprojecting to", srs)
    reprojected = f[:-4] + "_reprojected.shp"
    ogrCmd = ["ogr2ogr", workingDir + "/" + reprojected, workingDir + "/" + f, "-t_srs", "EPSG:4326"]
#    print(ogrCmd)
    subprocess.call(ogrCmd)
  return reprojected





if __name__ == "__main__":
  main()
