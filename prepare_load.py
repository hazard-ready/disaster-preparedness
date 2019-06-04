import os

from django.core.files import File
from disasterinfosite.models import PreparednessAction
from load_helpers import runLoader

currentPath = os.path.dirname(__file__)
appName = "disasterinfosite"
appDir = os.path.join(currentPath, "disasterinfosite")
dataDir = os.path.join(appDir, "data")
imagesDir = os.path.join(dataDir, 'images/prepare')
file = os.path.join(dataDir, "prepare.xlsx")

requiredFields = ['section', 'cost', 'text', 'external_text', 'external_link']
optionalFields = ['image', 'happy', 'useful', 'property', 'external_icon']


def run():
  config = {
    'file': file,
    'required': requiredFields,
    'optional': optionalFields,
    'processRow': processRow
  }
  rowCount = runLoader(config)
  print("Preparedness load complete. Processed", rowCount, "rows in", file)


def processRow(row, overwriteAll):
  section = row['section']
  removeOld(section)
  kwargs = {
    'title': section,
    'cost': row['cost'],
    'happy_text': row['happy'],
    'useful_text': row['useful'],
    'property_text': row['property'],
    'content_text': row['text'],
    'link_text': row['external_text'],
    'link': row['external_link']
  }
  pa = PreparednessAction.objects.create(**kwargs)
  pa.save()

  if row["image"] != '':
    imageFile = os.path.join(imagesDir, row["image"])
    with open(imageFile, 'rb') as f:
      data = File(f)
      pa.image.save(row["image"], data, True)

  if row["external_icon"] != '':
    imageFile = os.path.join(imagesDir, row["external_icon"])
    with open(imageFile, 'rb') as f:
      data = File(f)
      pa.link_icon.save(row["external_icon"], data, True)

  print('Created preparedness section:', pa.title)

def removeOld(section):
  if PreparednessAction.objects.filter(title__iexact=section).exists():
    PreparednessAction.objects.filter(title__iexact=section).delete()
