# FROM python:3.5-slim-buster
# FROM python:3.6-slim-buster
# FROM python:3.7-slim-bullseye
# FROM python:3.8-slim-bullseye
FROM python:3.9-slim-bullseye
# FROM python:3.10-slim-bullseye
# FROM python:3.11-rc-slim

ARG DJANGO_SECRET_KEY
ARG DATABASE_URL

ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
ENV DATABASE_URL=${DATABASE_URL}

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install GDAL dependencies
RUN apt-get update &&\
    apt-get install -y libgdal-dev g++ --no-install-recommends && \
    apt-get clean -y

# Update C env vars so compiler can find gdal
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

RUN apt-get install -y binutils libproj-dev gdal-bin libjpeg-dev

# Run the application:
COPY disasterinfosite /disasterinfosite
WORKDIR /disasterinfosite

# Install dependencies - added the ignore:DEPRECATION for python 3.5:
COPY requirements.txt .
RUN PYTHONWARNINGS="ignore:DEPRECATION" pip install --upgrade pip
RUN PYTHONWARNINGS="ignore:DEPRECATION" pip install --no-cache-dir -r requirements.txt

CMD ["python", "manage.py", "migrate"]
CMD ["python", "wsgi.py"]
