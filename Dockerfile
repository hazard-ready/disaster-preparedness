FROM python:3.9-slim-bullseye

ARG DJANGO_SECRET_KEY
ARG DATABASE_URL

ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY:-"dummykeyforbuild"}
ENV DATABASE_URL=${DATABASE_URL:-postgres://postgres:postgres@localhost:5432/pdxready}

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
RUN npm install && npm run webpack

WORKDIR /app

EXPOSE 8000

# Run the application:
# ENTRYPOINT ["python"]
# CMD ["manage.py", "runserver", "0.0.0.0:8000"]
# ENTRYPOINT ["/usr/local/bin/gunicorn"]
ENTRYPOINT ["/home/django/.local/bin/gunicorn"]
CMD ["--log-file=-", "--bind", ":8000", "--workers", "3", "disasterinfosite.wsgi:application"]
