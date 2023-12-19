import os

from django.core.files import File
from django.core.management.base import BaseCommand

from disasterinfosite.models import DataOverviewImage
from disasterinfosite.management.commands._load_helpers import (
    runLoader,
    includeTranslatedFields
)
from disasterinfosite.settings import BASE_DIR

appName = "disasterinfosite"
dataDir = os.path.join(BASE_DIR, "data")
imagesDir = os.path.join(dataDir, 'images/data_overview')
file = os.path.join(imagesDir, "data_overview.xlsx")

optionalFields = [
    'caption-es',
    'caption-cn',
    'caption-ru',
    'caption-so',
    'caption-vi',
    'caption-ar',
    'caption-ko'
]
def run():
    print("Deleting old Data Overview Images first.")
    DataOverviewImage.objects.all().delete()

    config = {
        'file': file,
        'optional': optionalFields,
        'processRow': processRow
    }
    rowCount = runLoader(config)

    print("Data overview image load complete. Processed", rowCount, "rows in", file)

def processRow(row, overwriteAll):
    kwargs = {
        'link_text': row['caption']
    }

    kwargs = includeTranslatedFields(row, 'caption', 'link_text', kwargs)
    overview_image = DataOverviewImage.objects.create(**kwargs)
    overview_image.save()

    thumbnail_name = row['filename'] + '.jpg'
    imageFile = os.path.join(imagesDir, thumbnail_name)
    with open(imageFile, 'rb') as f:
        data = File(f)
        overview_image.image.save(thumbnail_name, data, True)

    pdf_name = row['filename'] + '.pdf'
    pdfFile = os.path.join(imagesDir, pdf_name)
    with open(pdfFile, 'rb') as f:
        data = File(f)
        overview_image.pdf.save(pdf_name, data, True)

    print("created overview image", overview_image)

class Command(BaseCommand):
    help = """ Load data overview images found in data/images/data_overview/data_overview.xlsx """

    def handle(self, *args, **options):
        run()
