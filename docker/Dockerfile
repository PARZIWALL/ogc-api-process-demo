FROM geopython/pygeoapi:latest

USER root

RUN apt-get update && apt-get install -y \
    python3-geopandas \
    python3-shapely \
    python3-pyproj \
    python3-fiona \
    python3-requests \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/pygeoapi:$PYTHONPATH
