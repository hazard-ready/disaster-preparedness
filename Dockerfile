FROM python:3.11.3-slim-bullseye

ARG DJANGO_SECRET_KEY
ARG DATABASE_URL

ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
ENV DATABASE_URL=${DATABASE_URL}

# Update C env vars so compiler can find gdal
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Install GDAL dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    binutils          \
    libproj-dev       \
    gdal-bin          \
    libjpeg-dev       \
    g++               \
    libgdal-dev       \
    nodejs            \
    npm               \
    postgresql-client \
    unzip             \
    zip               \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r django && useradd --no-log-init -r -g django django
RUN mkdir /home/django && chown -R django:django /home/django
RUN mkdir /app

# copy the application to the container:
COPY . /app
RUN chown -R django:django /app
WORKDIR /app

USER django

# Install dependencies:
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# verify pip install
RUN pip list


# build front-end code
WORKDIR /app/disasterinfosite
RUN mkdir -p media/img/photos
RUN mkdir -p media/img/data
RUN unzip data.zip

RUN npm install && npm run webpack

# build translated files
RUN python ../manage.py makemessages -a
RUN python ../manage.py compilemessages

WORKDIR /app

RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Run the application:
ENTRYPOINT ["/home/django/.local/bin/gunicorn"]
CMD ["--log-file=-", "--bind", ":8000", "--workers", "3", "disasterinfosite.wsgi:application"]
