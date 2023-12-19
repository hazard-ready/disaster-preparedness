FROM python:3.12.1-slim-bookworm

ARG DJANGO_SECRET_KEY
ARG DATABASE_URL
ARG EMAIL_HOST
ARG EMAIL_HOST_USER
ARG EMAIL_HOST_PASSWORD

ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY:-"dummykeyforbuild"}
ENV DATABASE_URL=${DATABASE_URL:-postgres://postgres:postgres@localhost:5432/seattleready}
ENV EMAIL_HOST=${EMAIL_HOST}
ENV EMAIL_HOST_USER=${EMAIL_HOST_USER}
ENV EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD}

# Update C env vars so compiler can find gdal
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Get stuff we need to install Node and other dependencies
RUN apt-get update && apt-get upgrade -yqq && apt-get install -yqq wget gnupg

# Include PPA for latest Node version, then install GDAL and front-end dependencies
RUN echo "deb https://deb.nodesource.com/node_19.x bullseye main" > /etc/apt/sources.list.d/nodesource.list && \
  wget -qO- https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - && \
  apt-get update && apt-get upgrade -yqq && \
  apt-get install -y --no-install-recommends \
    binutils          \
    libproj-dev       \
    gdal-bin          \
    libjpeg-dev       \
    gettext           \
    g++               \
    libgdal-dev       \
    nodejs            \
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

# unzip data
WORKDIR /app/disasterinfosite
RUN rm -rf data && unzip -o data.zip

# build front-end code
RUN mkdir -p media/img/photos
RUN mkdir -p media/img/data

RUN npm rebuild node-sass
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
