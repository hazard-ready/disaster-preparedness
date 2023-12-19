import os

from django.core.files import File
from django.core.management.base import BaseCommand

from disasterinfosite.models import PreparednessAction, PreparednessLink
from disasterinfosite.management.commands._load_helpers import (
    runLoader,
    includeTranslatedFields
)
from disasterinfosite.settings import BASE_DIR

appName = "disasterinfosite"
dataDir = os.path.join(BASE_DIR, "data")
imagesDir = os.path.join(dataDir, 'images/prepare')
file = os.path.join(dataDir, "prepare.xlsx")

# All other fields are required
# Translated fields, like happy-es, happy-vi, etc will need to be added here
optionalFields = [
    'image',
    'happy',
    'useful',
    'property',
    'external_icon',
    'external_link_2',
    'external_text_2',
]


def run():
    config = {
        'file': file,
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
        'slug': row['slug']
    }

    kwargs = includeTranslatedFields(row, 'section', 'title', kwargs)
    kwargs = includeTranslatedFields(row, 'text', 'content_text', kwargs)
    kwargs = includeTranslatedFields(row, 'happy', 'happy_text', kwargs)
    kwargs = includeTranslatedFields(row, 'useful', 'useful_text', kwargs)
    kwargs = includeTranslatedFields(row, 'property', 'property_text', kwargs)

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

    link_kwargs = {
        'text': row['external_text_1'],
        'url': row['external_link_1'],
        'action': pa
    }
    link_kwargs = includeTranslatedFields(
        row, 'external_text_1', 'text', link_kwargs)
    link = PreparednessLink.objects.create(**link_kwargs)

    # an optional second link
    if row["external_text_2"]:
        link_kwargs = {
            'text': row['external_text_2'],
            'url': row['external_link_2'],
            'action': pa
        }
        link_kwargs = includeTranslatedFields(
            row, 'external_text_2', 'text', link_kwargs)
        link = PreparednessLink.objects.create(**link_kwargs)

    print('Created preparedness section:', pa.title)


def removeOld(section):
    if PreparednessAction.objects.filter(title__iexact=section).exists():
        PreparednessAction.objects.filter(title__iexact=section).delete()


class Command(BaseCommand):
    help = """ Load preparation information found in data/prepare.xlsx """

    def handle(self, *args, **options):
        run()
