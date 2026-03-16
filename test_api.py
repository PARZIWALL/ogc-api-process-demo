import requests
import json

def test_stac_buffer():
    url = "http://localhost:5000/processes/buffer-analysis/execution"
    payload = {
        "inputs": {
            "distance": 500,
            "stac_item_url": "https://raw.githubusercontent.com/radiantearth/stac-spec/master/examples/core-item.json"
        }
    }
    
    print(f"Sending POST request to {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        print(f"HTTP Status: {response.status_code}")
        
        if response.status_code in (200, 201):
            result = response.json()
            # print output summary rather than full geometry
            geom = result.get("geometry", result) if isinstance(result, dict) else result
            geom_type = geom.get("type", "Unknown") if isinstance(geom, dict) else "Unknown"
            print(f"Resulting Geometry Type: {geom_type}")
            print("Job Executed successfully!")
        else:
            print(f"Error Response: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_stac_buffer()
