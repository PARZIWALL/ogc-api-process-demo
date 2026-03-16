import logging
import requests
from pygeoapi.process.base import BaseProcessor, ProcessorExecuteError
import geopandas as gpd
from shapely.geometry import shape, mapping


LOGGER = logging.getLogger(__name__)

PROCESS_METADATA = {
    "version": "0.1.0",
    "id": "buffer-analysis",
    "title": "STAC Item Buffer Generator",
    "description": "Fetches a remote STAC Item, extracts its geometry, and creates a spatial buffer.",
    "keywords": ["buffer", "stac", "polygon", "geoprocessing"],
    "links": [{
        "type": "text/html",
        "rel": "about",
        "title": "information",
        "href": "https://example.org/process",
        "hreflang": "en-US"
    }],
    "inputs": {
        "distance": {
            "title": "Buffer distance",
            "description": "Distance in meters (projects to EPSG:3857 for buffering, then back to WGS84)",
            "schema": {
                "type": "number",
                "default": 100
            },
            "minOccurs": 1,
            "maxOccurs": 1
        },
        "stac_item_url": {
            "title": "STAC Item URL",
            "description": "URL to a STAC Item JSON (e.g. from Earth Search or Microsoft Planetary Computer)",
            "schema": {
                "type": "string",
                "format": "uri"
            },
            "minOccurs": 1,
            "maxOccurs": 1
        }
    },
    "outputs": {
        "result": {
            "title": "Buffered geometry",
            "description": "Buffered geometry in GeoJSON format",
            "schema": {
                "type": "object",
                "contentMediaType": "application/geo+json"
            }
        }
    },
    "example": {
        "inputs": {
            "distance": 500,
            "stac_item_url": "https://earth-search.aws.element84.com/v1/collections/sentinel-2-l2a/items/S2A_31UFU_20230815_0_L2A"
        }
    }
}


class ParkBuffer(BaseProcessor):
    """STAC Buffer Processor"""

    def __init__(self, processor_def):
        super().__init__(processor_def, PROCESS_METADATA)

    def execute(self, dict_data, **kwargs):
        distance = dict_data.get("distance", 100)
        stac_item_url = dict_data.get("stac_item_url")

        if not stac_item_url:
            raise ProcessorExecuteError("Missing required parameter: 'stac_item_url'")

        try:
            # Fetch STAC Item
            response = requests.get(stac_item_url, timeout=10)
            response.raise_for_status()
            stac_item = response.json()
            
            geometry_data = stac_item.get("geometry")
            if not geometry_data:
                raise ProcessorExecuteError("STAC Item does not contain a valid geometry.")

            # Parse input geometry
            geom = shape(geometry_data)
            
            # Create a GeoDataFrame from the input geometry (STAC items are WGS84 - EPSG:4326)
            gdf = gpd.GeoDataFrame(geometry=[geom], crs="EPSG:4326")
            
            # Project to a metric CRS (Web Mercator)
            gdf_projected = gdf.to_crs("EPSG:3857")
            
            # Perform Buffer
            gdf_buffered = gdf_projected.buffer(distance)
            
            # Project back to WGS84
            gdf_buffered_wgs84 = gdf_buffered.to_crs("EPSG:4326")
            
            # Extract resulting geometry
            result_geom = mapping(gdf_buffered_wgs84.iloc[0])

            mimetype = "application/geo+json"
            
            return mimetype, result_geom
            
        except requests.exceptions.RequestException as e:
            LOGGER.error(f"HTTP Request failed: {e}")
            raise ProcessorExecuteError(f"Failed to fetch STAC Item from URL: {str(e)}")
        except Exception as e:
            LOGGER.error(f"Processing error: {e}")
            raise ProcessorExecuteError(f"Error processing the STAC item: {str(e)}")
