from pygeoapi.process.base import BaseProcessor


PROCESS_METADATA = {
    "id": "park-buffer",
    "title": "Park Buffer Generator",
    "description": "Creates a buffer around park geometries",
    "inputs": {
        "distance": {
            "title": "Buffer distance",
            "description": "Distance in meters",
            "schema": {
                "type": "number"
            }
        }
    },
    "outputs": {
        "result": {
            "title": "Buffered geometry",
            "description": "Buffered parks in GeoJSON",
            "schema": {
                "type": "object"
            }
        }
    }
}


class ParkBuffer(BaseProcessor):

    def __init__(self, processor_def):
        super().__init__(processor_def, PROCESS_METADATA)

    def execute(self, data, **kwargs):
        distance = data.get("distance", 100)

        return "application/json", {
            "message": "buffer executed",
            "distance": distance
        }
