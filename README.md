# OGC API - Processes: Backend Demonstration

This repository contains a robust backend service implementing the **Open Geospatial Consortium (OGC) API – Processes** standard, built using [pygeoapi](https://pygeoapi.io/).

This project was built as a proof-of-concept for the 52°North GSoC 2024 selection process.

## 🚀 Unique Feature: Native STAC Integration
Most OGC API Processes demos rely on uploading raw GeoJSONs to the execution endpoint. Instead of passing bulk geometry data directly over the API, this backend introduces a **Native SpatioTemporal Asset Catalog (STAC) Processing handler**. 

The process accepts a remote STAC Item URL natively (e.g. from Earth Search or Microsoft Planetary Computer), streams the metadata over HTTP, performs geometric analysis safely via Web Mercator projection approximations, and returns a processed output mapped back to standard WGS84 for seamless web ingestion.

## ⚙️ Architecture
*   **Core**: Python 3.x
*   **Geoprocessing Engine**: GeoPandas, Shapely, PyProj.
*   **Web Framework**: pygeoapi (Geopython).
*   **Job Management**: Asynchronous processing enabled via TinyDB.
*   **Deployment**: Docker & Docker Compose.

## 🏗️ Getting Started

### 1. Build and Run the Container
You will need Docker Desktop or docker-compose installed.

```bash
cd docker
docker compose up -d --build
```

The api will be available at `http://localhost:5000`. Give it a few seconds to boot.

### 2. Verify the Endpoints
You can discover the API endpoints matching the OGC specifications:
*   **Landing Page**: `http://localhost:5000/`
*   **Process Definitions**: `http://localhost:5000/processes`
*   **Buffer Analysis STAC Process**: `http://localhost:5000/processes/buffer-analysis`
*   **Async Job Status Tracking**: `http://localhost:5000/jobs`

### 3. Execute the Sample Process
We can test the entire lifecycle, validating input parameters, processing the execution, and delivering the OGC API response.

Send a POST request to `/processes/buffer-analysis/execution`. We will use a public RadiantEarth STAC Item as a test payload:

```bash
curl -X POST "http://localhost:5000/processes/buffer-analysis/execution" \
     -H "Content-Type: application/json" \
     -d '{
           "inputs": {
             "distance": 500,
             "stac_item_url": "https://raw.githubusercontent.com/radiantearth/stac-spec/master/examples/core-item.json"
           }
         }'
```

You will receive an HTTP 200/201 response with the successfully buffered `Polygon` geometry dynamically extracted and processed from the remote catalog item!
