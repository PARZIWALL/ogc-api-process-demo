from pygeoapi.process.base import BaseProcessor


PROCESS_METADATA = {
    "id": "park-coolspot",
    "title": "Park Coolspot Detector",
    "description": "Detects potential cool spots inside parks",
    "inputs": {},
    "outputs": {
        "result": {
            "title": "Coolspot result",
            "schema": {
                "type": "object"
            }
        }
    }
}


class ParkCoolSpot(BaseProcessor):

    def __init__(self, processor_def):
        super().__init__(processor_def, PROCESS_METADATA)

    def execute(self, data, **kwargs):
        return "application/json", {
            "message": "coolspot executed"
        }
