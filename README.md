# Earthquake Preparedness Web Interactive

The project will explore traditional and qualitative scoring assessments of “risk/resiliency   factors” associated with regional crisis preparedness and demonstrate how actionable steps in community engagement can create a different portrait of resiliency. Stories will engage examples of communities in distinct regions across Oregon facing knowable challenges in the event of a major earthquake.

# Dependencies
## Django Web Framework
* PostgresSQL

## GeoDjango Dependencies
* PostresSQL
  * GeoDjango has other dependencies.  [See this more complete list](https://docs.djangoproject.com/en/1.7/ref/contrib/gis/install/geolibs/) of required and optional additions.
  
  
# Note about Python Command Usage
Commands indicated are always just `python` but on some systems you might need to use `python3` in order to use a specific python version.  If so, other commands such as `pip` have a `pip3` equivalent.

Use whichever base command is appropriate for your environment.
  
# Configure Dev Environment
Set up a virtual environment so that you can freely install python modules without worrying about overwriting globally installed versions.  It's easy!

1. `pip install virtualenv` (for python3, `pip3 install virtualenv`)
2. Move to the project directory (e.g. `/Applications/MAMP/htdocs/disaster-preparedness`).
3. `virtualenv --python=python3 venv --no-site-packages` 
4. Wait for things to happen.
5. `source venv/bin/activate`  (type `deactivate` to leave)
6. `pip install -r requirements.txt` or `pip3 install -r requirements.txt` to automatically install the Python dependencies listed in [requirements.txt](./requirements.txt). 

*On a Linux machine you may need to install `python-dev` (through the Linux package manager) as a prerequisite, and if you have trouble getting `psycopg2` to install you may have better luck using the package manager's version of that module.*  
 

# "World" App

**TODO: can we combine what are currently our "world" and "cascadiaprepared" folders, and get rid of the "aftershock" one entirely?**

Included is an app called World that was used to initially figure out
how GeoDjango works.  "Real" work will probably be taking place in another app
written slightly better and with all of the datasets modelled better.

## Written using:
* Postgres version: 9.4 
* Python version: 3.5

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
6. Run `python manage.py migrate` to initialize the database's structure.
7. Unzip `data.zip` inside world, so that the data is in `world/data`. This data includes some sample shapefiles and related data for Missoula County, Montana, USA, to get you started. See below for instructions on replacing this with your own data.
8. `python import.py` to process these shapefiles and update some Django code to fit. The script will prompt you for which field to use to look up snuggets (see below for definition), here is a list that corresponds to the sample data we have provided (shapefilename: fieldname):
    * `EQ_Fault_Buffer`: snugget_ID
    * `EQ_GroundShaking_MostLike`: Intensity
    * `EQ_Historic_Distance`: lookup_val
    * `Fire_hist_nrocky_1889_2003_all`: lookup_val
    * `Flood_FEMA_DFIRM_2015`: FEMADES
    * `MT_groundshaking`: intensity
9. `python manage.py makemigrations` - this and the next 2 steps combined load the new data into the database.
10. `python manage.py migrate`
11. `python manage.py shell`
    1. [inside the shell that this opens] `from world import load`
    2. `load.run()`
    3. `exit()` [to go back to the normal command line]
12. `python snugget_load.py` to import text that will be displayed in the site.  See below for an explanation of "snuggets" and the format of this file.
13. `python manage.py createsuperuser` and follow the instructions to add a Django admin user
14. If you don't already have web hosting set up, you can test your work on localhost:8000 with `python manage.py runserver`

#### Environmental Variable Permanence
On Linux/Mac, as soon as you close your shell you lose those nice complicated database urls.
Save them to your `.bash_profile` or equivalent.

### Create a user and visit the admin screen to verify
1. `python manage.py createsuperuser`
2. `python manage.py runserver` to run a development server on localhost:8000 or see below for how to deploy via Apache.
3. Visit http://server.ip/admin and log in with new user.
4. Should see a list of content.  *Don't try to directly edit data that came from the shapefiles - they are liable to be so complex with so many points that attempting this freezes or crashes the browser.*

### Deploying to the web via Apache

1. Install a version of `mod_wsgi` that is compiled for Python 3. On Debian/Ubuntu you can do this with `aptitude install libapache2-mod-wsgi-py3`. On other systems it may be easier to use `pip` as per [these instructions](https://pypi.python.org/pypi/mod_wsgi).
2. Use [these instructions](https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/modwsgi/) to configure Apache. Note in particular:
    1. You'll need `WSGIScriptAlias` to point to `cascadiaprepared/wsgi.py`
    2. You'll need to apply the "Using a virtualenv" addition.
    3. You'll need to set up a `/static/` alias pointing to `cascadiaprepared/static`
    4. Depending on your server configuration, you *may* also need to set up a redirect rule to add trailing slashes to URLs, to get the static files (CSS, images etc) included.
    5. You may also need to alter the `STATIC_URL` constant in `settings.py` based on your server setup
3. Set up the environment values from above (`DJANGO_SECRET_KEY` and `DATABASE_URL`) for all users by putting their declarations in `/etc/environment/` and rebooting the machine.

### Use foreman to run the server Heroku-style
*Not tested by the current maintainers*

* `foreman start`
  * Any errors that pop up are probably from missing modules or missing environmental variables. Read the errors!

## Adding new data

*Hooray!  Much of the process is now automated.  Still TODO: make this documentation clearer and add suggestions for less standardised content.*

0. Export a shapefile with an attribute that can be used to look up appropriate snugget text and intensity values for each shape. It can be in any SRS, and it doesn't matter if there are additional attributes, but be aware that those will be lost in the import. *Note that if you use multiple shapefiles that cover different areas (e.g. some cover a county and some cover a whole state), users will see partial results without a warning that there's missing data. For clearest results, crop all your shapefiles to the same area.*
1. Put it into `/world/data/`
2. [then skip to 8 of the initial deploy instructions]
8. [Re]start the web server *(TODO: figure out if there's a way to just get Django to restart without rebooting Apache/etc)*
9. Add manual snuggets if necessary.
10. test.
