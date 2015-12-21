import os
import subprocess
import sys

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
      print("Opening shapefile:", f[:-4])
      reprojected = reprojectShapefile(f, dataDir, reprojectedDir, "EPSG:4326")
      simplified = simplifyShapefile(reprojected, simplifiedDir, "0.0001")



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



if __name__ == "__main__":
  main()
