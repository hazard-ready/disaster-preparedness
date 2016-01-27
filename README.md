# Disaster Preparedness Web Interactive

The project will explore traditional and qualitative scoring assessments of “risk/resiliency factors” associated with regional crisis preparedness and demonstrate how actionable steps in community engagement can create a different portrait of resiliency. It is based on [a pioneering project from Oregon](https://github.com/Oregon-Public-Broadcasting/earthquake-preparedness) but has been generalized to make it easy to clone and tailor to other regions.

# Dependencies
* Django Web Framework
* GeoDjango
* PostgresSQL
* PostGIS
* Python modules listed in [requirements.txt](./requirements.txt)
  * On a Linux machine you may need to install `python-dev` (through the Linux package manager) as a prerequisite, and if you have trouble getting `psycopg2` to install you may have better luck using the package manager's version of that module.
  * GeoDjango has other dependencies, but if you install it from a package manager they will usually be included automatically.  [See this more complete list](https://docs.djangoproject.com/en/1.7/ref/contrib/gis/install/geolibs/) of required and optional additions.

# Note about Python Command Usage
Commands indicated are always just `python` but on some systems you might need to use `python3` in order to use a specific python version.  If so, other commands such as `pip` have a `pip3` equivalent.

Use whichever base command is appropriate for your environment.

# Configure Dev Environment
Set up a virtual environment so that you can freely install python modules without worrying about overwriting globally installed versions.  It's easy!

1. `pip install virtualenv` (for python3, `pip3 install virtualenv`)
2. Move to the project directory (e.g. `/Applications/MAMP/htdocs/disaster-preparedness`).
3. `virtualenv --python=python3 venv --no-site-packages`
4. Wait for things to happen.
5. `source venv/bin/activate`  (type `deactivate` to leave). Remember to reactivate the virtual environment every time you open a terminal window and start running Python commands.
6. `pip install -r requirements.txt` or `pip3 install -r requirements.txt` to automatically install the Python dependencies listed in [requirements.txt](./requirements.txt). You may see "Failed building wheel for ..." errors for some of the modules. If so, try repeating the command. If the second run shows "Requirement already satisfied" for every module then you can safely ignore the previous error.

# "disasterinfosite" App

While management and data loading files are in this project's root directory, everything else is in `/disasterinfosite`.

## Written using:
* Postgres version: 9.4
* Python version: 3.5

## File structure

* `/disasterinfosite/data` contains the shapefiles and text content (snuggets - see [Adding New Data](#adding-new-data) below for explanation) that will be loaded.
* `/disasterinfosite/migrations` contains Django-generated files that specify how to set the database up. We don't recommend editing these manually.
* `/disasterinfosite/static/css` contains all the stylesheets for this site.
* `/disasterinfosite/static/img` contains all the static images - if you want to change icons, etc, look here.
* `/disasterinfosite/static/js` contains JavaScript libraries that need to be included for various site functions.
* `/disasterinfosite/templates` and `/disasterinfosite/templatetags` contain HTML templates for the site's various pages and subsections, and Python code that processes them. Many of the simpler customizations to this site will involve editing the HTML templates.

## Installing App
This assumes `python` is the command configured to run the correct python version. Depending on your setup you may need to specify `python3`.

### Set up the "secret key" used by Django to secure forms.
* Set up an environment variable `DJANGO_SECRET_KEY` to whatever you want to set it to.
  * See http://techblog.leosoto.com/django-secretkey-generation/ for an example approach.
  * On Mac/Linux: `export DJANGO_SECRET_KEY="gibberishrandomstring"`

### Set up the database

1. Set up Postgres with PostGIS:
 * To install PostGIS on a Mac using Homebrew: `brew install postgis`. Here are [PostGIS install instructions for Ubuntu](https://trac.osgeo.org/postgis/wiki/UsersWikiPostGIS21UbuntuPGSQL93Apt).
 * The Mac or Ubuntu instructions will also install Postgres if you don't already have that.
 * Run `brew info postgres` to see options for starting Postgres - you can have it start automatically when your computer starts, or not.
 * Homebrew sets Postgres up with one user to start with, and that user is you. You should probably make a separate user for Django. If you want your user to be named `django`, do `createuser django --password`. You will then get a prompt for the password. Use only letters and numbers in the password, because you'll need to use it in a URL later.
2. Clone repo.
3. Create a Postgres database on the Postgres server, and install PostGIS to it.

    ```shell
    createdb [DBNAME]
    psql -d [DBNAME] -c "CREATE EXTENSION postgis;"
    ```
4. In order to run unit tests, your user will need to be able to create and delete databases, since the test framework creates (and destroys) a new test DB for each test run. You can accomplish this using ```psql -d [DBNAME] -c "ALTER USER [USERNAME] SUPERUSER;"
*[detailed instructions for reference](http://postgis.net/docs/manual-2.1/postgis_installation.html#create_new_db_extensions)*
5. Set up an environment variable `DATABASE_URL` that will be used by the Django Database URL app to load our database.
  * example on Mac/Linux: `export DATABASE_URL="postgres://USER:PASSWORD@HOST:PORT/DBNAME"` where the USER & PASSWORD are the django account you created above in postgres, and the default HOST:PORT is localhost:5432 .
6. `source venv/bin/activate` if you haven't already activated the virtualenv this session.
7. Run `python manage.py migrate` to initialize the database's structure.

### Load some data
0. `source venv/bin/activate` if you haven't already activated the virtualenv this session.
1. Unzip `data.zip` inside disasterinfosite, so that the data is in `disasterinfosite/data`. This data includes some sample shapefiles and related data for Missoula County, Montana, USA, to get you started. See below for instructions on replacing this with your own data.
2. `python import.py` to process these shapefiles and update some Django code to fit. The script will prompt you for which field to use to look up snuggets (see [Adding New Data](#adding-new-data) below for definition). If you use the example `data.zip` provided in this project, use the field name `lookup_val` for every shapefile except `Flood_FEMA_DFRIM_2015`, for which you should use `FEMADES`.
3. `python manage.py makemigrations` - this and the next 2 steps combined load the new data into the database.
4. `python manage.py migrate`
5. `python manage.py shell`
    1. [inside the shell that this opens] `from disasterinfosite import load`
    2. `load.run()`
    3. `exit()` [to go back to the normal command line]
6. `python snugget_load.py` to import text that will be displayed in the site.  See [Adding New Data](#adding-new-data) below for an explanation of "snuggets" and the format of this file.
7. If this is your first time through, or you emptied the database before loading new data: `python manage.py createsuperuser` and follow the instructions to add a Django admin user
8. If you don't already have web hosting set up, you can test your work on localhost:8000 with `python manage.py runserver`

#### Environmental Variable Permanence
On Linux/Mac, as soon as you close your shell you lose those nice complicated database urls.
Save them to your `.bash_profile` or equivalent.

### Create a user and visit the admin screen to verify
1. `python manage.py createsuperuser`
2. `python manage.py runserver` to run a development server on localhost:8000 or see below for how to deploy via Apache.
3. Visit http://server.ip/admin and log in with new user.
4. You should see a list of content.  *Don't try to directly edit data that came from the shapefiles - they are liable to be so complex with so many points that attempting this freezes or crashes the browser.* **TODO: Do those shapefiles need to show up in here at all?**
5. There are other pieces of content that you can and should edit, though! They are bits of text and other information that show up on this site.
  1. **Important Links** - Add as many of these as you want. They show up under 'Important Links' when location-specific information is found. You can put any text in the 'link' field and web addresses are turned into links automatically. The title shows up in bold over each link.
  1. **Location Information** - Area Name shows up all over the place, especially in the instructions on the home page. 'Community leaders' appears under location-specific information.
  1. **Site Settings** - Basic information about this site and who created it. This stuff shows up in the page headers and footers. The 'who made this' section especially deserves lots of details, and the Data Download link is if you'd like to share the data that you used to create this site. The site title is the big text at the top.
  1. **Supply Kit** - The numbers in the supply kit information is based on the number you enter here for 'days', and the text can be anything you like.

### Deploying to the web via Apache

1. Install a version of `mod_wsgi` that is compiled for Python 3. On Debian/Ubuntu you can do this with `aptitude install libapache2-mod-wsgi-py3`. On other systems it may be easier to use `pip` as per [these instructions](https://pypi.python.org/pypi/mod_wsgi).
2. Use [these instructions](https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/modwsgi/) to configure Apache. Note in particular:
    1. You'll need `WSGIScriptAlias` to point to `disasterinfosite/wsgi.py`
    2. You'll need to apply the "Using a virtualenv" addition.
    3. You'll need to set up a `/static/` alias pointing to `disasterinfosite/static`
    4. Depending on your server configuration, you *may* also need to set up a redirect rule to add trailing slashes to URLs, to get the static files (CSS, images etc) included.
    5. You may also need to alter the `STATIC_URL` constant in `settings.py` based on your server setup.
3. Set up the environment values from above (`DJANGO_SECRET_KEY` and `DATABASE_URL`) for all users by putting their declarations in `/etc/environment/` and rebooting the machine.

### Use foreman to run the server Heroku-style
*Not tested by the current maintainers*

* `foreman start`
  * Any errors that pop up are probably from missing modules or missing environmental variables. Read the errors!

## Adding new data

### What you need

1. At least one shapefile, meeting the following requirements:
    1. Each shapefile's attribute table must contain a column with a unique identifier for each set of text to display (e.g. all the areas for which you want to display "Expected ground shaking: severe" have one ID, and all the areas for which you want to display "Expected ground shaking: moderate" have another). This column will be used to look up text when a user selects a location.
    2. That column's name must comply with the [Django field name restrictions](https://docs.djangoproject.com/en/1.9/topics/db/models/#field-name-restrictions), including not being one of the [Python 3 reserved words](https://stackoverflow.com/questions/22864221/is-the-list-of-python-reserved-words-and-builtins-available-in-a-library/22864250#22864250). For example, if the column is called `id`, `object`, `map`, `property` or `type`, you'll have to rename it.
    3. It doesn't matter which coordinate reference system the shapefile has been saved with, but if you're making them yourself then we recommend using EPSG:4326, because the import pipeline will reproject it to that anyway.
    4. If you have multiple shapefiles, clip them all to cover the same area. Otherwise, if users click on a location that is covered by some shapefiles but not others they will see partial data without a clear explanation that there is missing data.
    5. Multiple shapes may overlap, but each shape may only have one value for the lookup field. If you have multiple shapes with the same lookup value, the import process will combine them.
2. Some text content to display when a user chooses a location in one or more of your shapefiles. In this project, the text content is referred to as **snuggets**, from "story nuggets".

If you have raster data, first convert it to a shapefile.  See [Converting raster files](#converting-raster-files) below for pointers if you don't already know how to do that.

### Fully automated pipeline

If the structure of your text content is simple enough, you can import shapefiles and snuggets automatically without having to do much manual work. We recommend using this pathway if possible, because it makes moving the site to a new server significantly easier. To do this, you will need a `snuggets.csv` file with the same columns as the example one we've included in `data.zip`.  The columns can be in any order, but the headings must be exactly as typed here:

* `section` : A section name that will be displayed on the page (must not be empty)
* `subsection` : A subsection name (must not be empty)
* `shapefile` : The file name for the shapefile this row corresponds to, without the extenstion. For example: `EQ_GroundShaking_MostLike` for text that relates to the content of `EQ_GroundShaking_MostLike.shp`. (must not be empty; must correspond exactly to the available shapefiles)
* `heading` : A human-readable heading that describes the content of this shapefile, to be displayed on the page.
* `lookup_value` : The value of the unique identifier in the shapefile (e.g. an intensity value or a hazard classification). This field can be empty; if it is then the rest of this row will be applied to every available value.
* `intensity` : Relative severity scaled from 0-100, to display graphically on the page. If this is empty, or if a value is provided for `image`, it will simply not be displayed.
* `image` : The file name for an image, stored in `disasterinfosite/static/img`, that illustrates the severity. If this is empty it won't be displayed. If there is a value here (including '0' or NULL), it overrides the value of `intensity`.
* `text` : The explanatory text to be displayed in the relevant section and subsection when the user chooses a location that matches this row's criteria. If you put a url in the snugget text, like `http://www.github.com`, we'll automatically make it into a link for you.

You can have any number of sections and subsections, but every row must be a unique combination of `shapefile`, `section`, `subsection` and `lookup_value`. If you define more than one row for the same permutation, only the last one in the file will actually be used. Note that this allows you to create a default value for a given section, subsection and shapefile, by having a row with `lookup_value` blank (so it applies to all values present in the shapefile), followed by rows with specified `lookup_value`s which will overwrite the default for that value only.

Blank rows or additional columns won't cause problems. Any row that is missing any of the required fields will be skipped and a warning will be printed.

Once `snuggets.csv` is ready, simply put it and the relevant shapefiles in `disasterinfosite/data` (and remove any other files or subdirectories from there), and follow the instructions in [Load Some Data](#load-some-data) above.

#### Updating existing data

If you make changes to `snuggets.csv` you should only need to re-run `python snugget_load.py` and restart your web server.

If you make changes to the shapefiles, or change which field from the shapefiles you want to use as the ID, then before running `python import.py` you will also need to remove the `disasterinfosite/data/reprojected` and `word/data/simplified` directories that the importer had created. It uses these to avoid having to repeat the time-consuming reprojection and simplification of the shapefiles every time it is run, but that means changes to the shapefiles themselves won't be picked up unless they are removed.

If you have existing data that needs to be removed—perhaps because you are replacing our sample data, or retiring a shapefile you previously used—you may have to clear the database first.  To do this:

1. `psql -d [DBNAME] -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public; CREATE EXTENSION postgis;"`
2. `python manage.py migrate` - if this step throws errors, delete all the .py files in `disasterinfosite/migrations` **except** `__init__.py` and `0001_initial.py`, and try again.

Then continue with the instructions in [Load Some Data](#load-some-data) above.

### Working with more complex text templates

You may want to use multiple fields from a shapefile to fill in blanks from a template, such as "In year [YEAR] the [FIRENAME] fire burned [AREA] acres here". The automated import pipeline is not sophisticated enough to do this for you, so you have two options:

#### If you can edit the shapefile

Using QGIS or ArcGIS, add two columns to the shapefile: one with a lookup value composed of all the variables you're using (e.g. `[FIRENAME]_[YEAR]_[AREA]`), and one with the complete text. You can create both of these using calculdated fields in either program. Then copy-paste the attribute table into Excel or an equivalent, and use the complete texts to populate the `text` column of `snuggets.csv` and the lookup values for the `lookup_value` column. With this, you can use the automated pipeline to do the rest.

#### If you can't edit the shapefile, or are more comfortable editing code

Take a look at `disasterinfosite/models.py`, `disasterinfosite/load.py` and `disasterinfosite/admin.py` after running the automated pipeline on some sample data, and write appropriate equivalents for all of the generated code (marked by prominent comments) that fit your data and text model. You may also need to edit `disasterinfosite/templates/found_content.html` which is the page template to be displayed when there is at least one snugget available for a location. Then run just the `manage.py` parts of the [Load Some Data](#load-some-data), and use the Django admin panel to enter snuggets by hand.

If you have some data that fits that automated import model and some that does not, you can combine the two. Just watch for three things:

1. You'll have to reproject the shapefiles that aren't going through the import pipeline to EPSG:4326 yourself.
2. Put the shapefiles that aren't being manually imported somewhere other than `disasterinfosite/data` to keep them out of the automated pipeline.
3. Be very careful to avoid putting any of your manually edited code between the `# GENERATED CODE GOES HERE` and `# END OF GENERATED CODE BLOCK` comment pairs in the Python files, because that part gets overwritten by `import.py` each time.

### Converting raster files

The import pipeline doesn't currently have a way to handle raster data. Instead you'll have to convert the file to vector data first, and save the shapefile this creates in `disasterinfosite/data`. Here are three ways to do that:

#### Using GDAL from the command line

GDAL includes a [polygonize](http://www.gdal.org/gdal_polygonize.html) tool. If you have this available, then simply run:

```shell
gdal_polygonize.py RASTERFILENAME.tif -f 'ESRI Shapefile' OUTPUTFILENAME.shp
```

This is the preferred method if you already have GDAL installed, but if you don't then be aware that installing GDAL can be complicated.

The output file will have an attribute `DN` that contains the pixel values from the raster file.

#### Using QGIS

* Open the raster file in QGIS
* Choose `Raster > Conversion > Polygonize` from the menus
* Use the Select button by "Output file" to give this a destination in `disasterinfosite/data`, and leave the other options as they are
* Click "OK" and be warned that it may take a while
* When it's finished, check the shapefile it's created.  It likes to create lines instead of polygons - if it did that, then use `Vector > Geometry Tools > Lines to Polygons` to make an actual polygons file, and take the lines file out of `disasterinfosite/data`.

The output file will have an attribute `DN` that contains the pixel values from the raster file.

#### Using ArcGIS

Try [these instructions](http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#/Raster_to_Polygon/001200000008000000/).


