# Earthquake Preparedness Web Interactive

The project will explore traditional and qualitative scoring assessments of “risk/resiliency   factors” associated with regional crisis preparedness and demonstrate how actionable steps in community engagement can create a different portrait of resiliency. Stories will engage examples of communities in distinct regions across Oregon facing knowable challenges in the event of a major earthquake.

# Dependencies
## Django Web Framework
* PostgresSQL
  * PostgresSQL in Django requires psycopg2 (but maybe we end up bypassing this or something with PostGIS?)

## GeoDjango Dependencies
* PostresSQL
  * GeoDjango has other dependencies.  [See this more complete list](https://docs.djangoproject.com/en/1.7/ref/contrib/gis/install/geolibs/) of required and optional additions.

# "World" App
Included is an app called World that was used to initially figure out
how GeoDjango works.  "Real" work will probably be taking place in another app
written slightly better and with all of the datasets modelled better.
## Written using:
* Postgres version: 9.4 
* Python version: 3.4

## Installing App
This assumes 'python' is the command configured to run the correct python version.

### Set up the database
1. Clone repo.
2. Create a Postgres database on the Postgres server.
3. Copy contents of cascadiaprepared/secure_settings.py.template to cascadiaprepared/secure_settings.py
4. Update secure_settings.py to point this django project to the correct databae.
5. Generate a secret key and put it into the appropriate secure_settings.py variable.
  * See [google for ideas](https://www.google.com/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#q=django+generate+secret+key]) 
  * Run `python manage.py migrate` to initialize the database's structure.
6. Unzip the TsunamiEvacuationZones_2013.zip and [TM_WORLD_BORDERS-0.3.zip](http://thematicmapping.org/downloads/TM_WORLD_BORDERS-0.3.zip) into world/data
7. Start a python shell with `python manage.py shell`
8. Type `from world import load` and then `load.run()` to import the shapefile data into the DB
9. Type `exit()` to exit the shell.

### Create a user and visit the admin screen to verify
1. `python manage.py createsuperuser`
2. `python manage.py runserver` (or configure another webserver) and visit http://server.ip/admin and log in with new user.
3. Should see a list of content.  *Don't try to edit any DOGAMI data directly; those shapes are so complex with so many points that it's a guaranteed browser crash/freeze.*

### Just check to see some very simple checking if a point falls within a shape in the DB
1.  Visit http://server.ip/zonecheck
