import os
from django.core.files import File
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from disasterinfosite.models import *
from disasterinfosite.settings import BASE_DIR
from disasterinfosite.management.commands._load_helpers import (
    XLSXDictReader,
    runLoader,
    includeTranslatedFields
)


appName = "disasterinfosite"
dataDir = os.path.join(BASE_DIR, "data")
snuggetFile = os.path.join(dataDir, "snuggets.xlsx")
# there can be multiple of these files in different locations,
# so the full path is assembled in addSlideshow()
slideshowFilename = "slideshow.xlsx"

# all other fields in snuggetFile are required.
# Note the last field - it's a translation column.
# Add languages and language codes as you see fit!
optionalFields = ['heading',
                  'intensity',
                  'lookup_value',
                  'txt_location',
                  'pop_out_image',
                  'pop_out_link',
                  'pop_alt_txt',
                  'pop_out_txt',
                  'pop_out_video',
                  'intensity_txt',
                  'text',
                  'image_slideshow_folder',
                  'video',
                  'text-es',
                  'pop_out_txt-es']

defaults = {
    "intensity": None,
    "pop_out_video": None,
    "txt_location": 0
}


def run():
    config = {
        'file': snuggetFile,
        'optional': optionalFields,
        'processRow': processRow
    }
    rowCount = runLoader(config)
    print("Snugget load complete. Processed", rowCount, "rows in", snuggetFile)


def setDefaults(row):
    for key, value in defaults.items():
        if row[key] == '':
            row[key] = value


def processRow(row, overwriteAll):
    shapefile = getShapefileClass(row)
    filterColumn = row["shapefile"] + "_filter"
    section, created = SnuggetSection.objects.get_or_create(
        name=row["section"])

    setDefaults(row)

    order = row["txt_location"]

    if created:
        print("Created a new snugget section: ", row["section"])

    # check if a snugget for this data already exists
    # if we have a lookup value then deal with this value specifically:
    if row["lookup_value"] != '':
        # if it is blank, we'll treat it as matching all existing values
        filterVal = getShapefileFilter(shapefile, row["lookup_value"])
        oldSnugget = checkForSnugget(
            shapefile, section, order, filterColumn, filterVal)
        overwriteAll = askUserAboutOverwriting(row, oldSnugget, overwriteAll)
        processSnugget(row, shapefile, section, order, filterColumn, filterVal)
    else:
        filterVals = findAllFilterVals(shapefile)
        oldSnuggets = []
        for filterVal in filterVals:
            oldSnugget = checkForSnugget(
                shapefile, section, order, filterColumn, filterVal)
            if oldSnugget is not None and oldSnugget not in oldSnuggets:
                oldSnuggets.append(oldSnugget)
            overwriteAll = askUserAboutOverwriting(
                row, oldSnuggets, overwriteAll)
            processSnugget(row, shapefile, section,
                           order, filterColumn, filterVal)

    return overwriteAll


def processSnugget(row, shapefile, section, order, filterColumn, filterVal):
    removeOldSnugget(shapefile, section, order, filterColumn, filterVal)
    if row["image_slideshow_folder"] != '':
        addSlideshowSnugget(row, shapefile, section, filterColumn, filterVal)
    elif row["video"] != '':
        addVideoSnugget(row, shapefile, section, filterColumn, filterVal)
    else:
        addTextSnugget(row, shapefile, section, filterColumn, filterVal)


def getShapefileClass(row):
    modelName = row["shapefile"].lower()
    if ContentType.objects.filter(app_label=appName, model=modelName).exists():
        shapefile = ContentType.objects.get(
            app_label=appName, model=modelName).model_class()
        return shapefile
    else:
        # nothing was found in the database for the shapefile name
        print("No shapefile with the name",
              row["shapefile"], "appears to have been loaded.")
        print("If the shapefile exists, you may still need to run the \
         migration and loading steps - see the 'Load some data' section of the readme file.")
        return None


def getFilterFieldName(shapefile):
    # The lookup value / filter field is the one from the shapefile
    # that is not one of these.
    field = next(f for f in shapefile._meta.get_fields()
                 if f.name not in ['id', 'geom', 'group'])
    return field.name


def getShapefileFilter(shapefile, filterVal):
    fieldName = getFilterFieldName(shapefile)
    if fieldName == 'rast':
        minima = [256]
        maxima = [0]
        for tile in shapefile.objects.all():
            if tile.rast.bands[0].min is not None:
                if int(filterVal) in tile.rast.bands[0].data():
                    return int(filterVal)
                minima.append(tile.rast.bands[0].min)
                maxima.append(tile.rast.bands[0].max)
        print(
            "Lookup value of", filterVal,
            "not found in", shapefile,
            ", which only has values between", str(min(minima)),
            "and", str(max(maxima)),
            "inclusive (and may not have all values in between)."
        )
    else:
        kwargs = {fieldName: filterVal}
        if shapefile.objects.filter(**kwargs).exists():
            return shapefile.objects.get(**kwargs)
        else:
            print("Could not find a filter field for", shapefile)
    return None


def addPopOutIfExists(row):
    if (row["pop_out_image"] != '' or
        row["pop_out_txt"] != '' or
        row["pop_alt_txt"] != '' or
        row["pop_out_link"] != '' or
            row["pop_out_video"] is not None):
        args = {'text': row["pop_out_txt"], 'alt_text': row["pop_alt_txt"],
                'link': row["pop_out_link"], 'video': row["pop_out_video"]}
        kwargs = includeTranslatedFields(row, 'pop_out_txt', 'text', args)
        popout = SnuggetPopOut.objects.create(**kwargs)
        if row["pop_out_image"] != '':
            imageFile = os.path.join(
                dataDir, 'images/pop_out', row["pop_out_image"])
            with open(imageFile, 'rb') as f:
                data = File(f)
                popout.image.save(row["pop_out_image"], data, True)

        return popout
    else:
        return None


def addTextSnugget(row, shapefile, section, filterColumn, filterVal):
    group = shapefile.getGroup()

    if filterVal is not None:
        args = {
            'section': section,
            'group': group,
            filterColumn: filterVal,
            'content': row["text"],
            'percentage': row["intensity"],
            'order': row['txt_location']
        }

        kwargs = includeTranslatedFields(row, 'text', 'content', args)
        snugget = TextSnugget.objects.create(**kwargs)
        snugget.pop_out = addPopOutIfExists(row)
        snugget.save()


def addVideoSnugget(row, shapefile, section, filterColumn, filterVal):
    group = shapefile.getGroup()

    args = {
        'section': section,
        'group': group,
        filterColumn: filterVal,
        'text': row["text"],
        'video': row["video"],
        'percentage': row["intensity"],
        'order': row['txt_location']
    }
    kwargs = includeTranslatedFields(row, 'text', 'text', args)

    snugget = EmbedSnugget.objects.create(**kwargs)
    snugget.save()


def addSlideshowSnugget(row, shapefile, section, filterColumn, filterVal):
    group = shapefile.getGroup()

    args = {
        'section': section,
        'group': group,
        filterColumn: filterVal,
        'text': row["text"],
        'percentage': row["intensity"],
        'order': row['txt_location']
    }

    kwargs = includeTranslatedFields(row, 'text', 'text', args)

    snugget = SlideshowSnugget.objects.create(**kwargs)
    snugget.pop_out = addPopOutIfExists(row)
    addSlideshow(os.path.join(dataDir, 'images/',
                              row["image_slideshow_folder"]), snugget)
    snugget.save()


def addSlideshow(folder, snugget):
    slideshowFile = os.path.join(folder, slideshowFilename)

    slides = XLSXDictReader(slideshowFile)
    # row 1 consists of field names, so row 2 is the first data row.
    # We'll increment this before first referencing it.
    rowCount = 1
    for row in slides:
        rowCount += 1
        photo = PastEventsPhoto.objects.create(
            snugget=snugget,
            caption=row["caption"],
            caption_es=row["caption-es"]
        )
        if row["image"] != '':
            imageFile = os.path.join(folder, row["image"])
            with open(imageFile, 'rb') as f:
                data = File(f)
                photo.image.save(row["image"], data, True)

    print("... Image slideshow created from", folder)


def findAllFilterVals(shapefile):
    fieldName = getFilterFieldName(shapefile)
    if fieldName == 'rast':
        # If it's a raster, we take a small shortcut and just return the whole
        # range of values from min to max, assuming all the intermediate ones
        # exist. This may create some surplus snuggets, but won't miss any
        # that should be there.
        minima = [256]
        maxima = [0]
        for tile in shapefile.objects.all():
            if tile.rast.bands[0].min is not None:
                minima.append(tile.rast.bands[0].min)
                maxima.append(tile.rast.bands[0].max)
        return list(range(min(minima), max(maxima)+1))
    else:
        return shapefile.objects.all()


def checkForSnugget(shapefile, section, order, filterColumn, filterVal):
    if filterVal is not None:
        kwargs = {'section': section, 'order': order, filterColumn: filterVal}
        if Snugget.objects.filter(**kwargs).exists():
            return Snugget.objects.select_subclasses().get(**kwargs)
    return None


def removeOldSnugget(shapefile, section, order, filterColumn, filterVal):
    kwargs = {'section': section, filterColumn: filterVal, 'order': order}
    Snugget.objects.filter(**kwargs).delete()


# Check with the user about overwriting existing snuggets,
# giving them the options to:
# either quit and check what's going on, or
# say "yes to all" and not get prompted again.
def askUserAboutOverwriting(row, old, overwriteAll):
    if overwriteAll:  # if it's already set, then don't do anything else
        return True
    else:
        if old is not None and not isinstance(old, list):
            print("In shapefile ",
                  repr(row["shapefile"]),
                  " there is already a snugget defined for section ",
                  repr(row["section"]),
                  ", intensity ", repr(
                      row["lookup_value"]),
                  ", txt_location ",
                  repr(row["txt_location"]),
                  " with the following text content:",
                  sep=""
                  )
            print(old)
        elif old and isinstance(old, list):
            print("In shapefile ",
                  repr(row["shapefile"]),
                  " there are existing snuggets for section",
                  repr(
                      row["section"]),
                  ", txt_location",
                  repr(row["txt_location"]),
                  " with the following text content:",
                  sep=""
                  )
            for snugget in old:
                print(snugget)
        else:
            # if no existing snuggets were found, then we neither need to ask
            # the user this time nor change overwriteAll
            return overwriteAll

        print("Please enter one of the following letters to choose how to proceed:")
        print("R: Replace the existing snugget[s] with the new value loaded from",
              snuggetFile, " and ask again for the next one.")
        print("A: replace All without asking again.")
        print("Q: quit so you can edit",
              snuggetFile,
              "and/or check the snuggets in the Django admin panel and try again.")
        response = ""
        while response not in ["A", "R", "Q"]:
            response = input(">> ").upper()

        if response == "Q":
            exit(0)
        elif response == "A":
            return True
        elif response == "R":
            return False


class Command(BaseCommand):
    help = """ Load snuggets found in data/snuggets.xlsx """

    def handle(self, *args, **options):
        run()
