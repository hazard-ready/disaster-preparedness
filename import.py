import os
import subprocess
import sys

def main():
  workingDir = "world/data"
  for f in os.listdir(workingDir):
    if f[-4:] == ".shp" and f[-16:] != "_reprojected.shp":
      print("Opening shapefile:", f[:-4])
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
