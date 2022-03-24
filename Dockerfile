FROM python:3.9-slim-bullseye

ARG DJANGO_SECRET_KEY
ARG DATABASE_URL

ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
ENV DATABASE_URL=${DATABASE_URL}

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install GDAL dependencies
RUN apt-get update && \
    apt-get install -y libgdal-dev g++ --no-install-recommends && \
    apt-get install -y postgresql-client && \
    apt-get clean -y

# Update C env vars so compiler can find gdal
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

RUN apt-get install -y binutils libproj-dev gdal-bin libjpeg-dev

# Run the application:
COPY . /app
WORKDIR /app

# Install dependencies:
COPY requirements.txt .
RUN /opt/venv/bin/pip install --upgrade pip
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# verify pip install
RUN /opt/venv/bin/pip list

EXPOSE 8000

CMD ["/opt/venv/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]
