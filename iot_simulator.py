import sys
import requests
import time
import random

URL = "http://127.0.0.1:8001/api/method/smart_bmr.smartbmr.doctype.batch_manufacturing_record.batch_manufacturing_record.log_machine_temperature"

if len(sys.argv) > 1:
    BMR_ID = sys.argv[1]
else:
    BMR_ID = "okjjuke1o1"

print(f"Starting IoT Simulation for {BMR_ID}...")

try:
    while True:
        simulated_temp = round(random.uniform(36.5, 40.5), 2)
        
        payload = {
            "bmr_id": BMR_ID,
            "temp_reading": simulated_temp
        }
        
        response = requests.post(URL, data=payload)
        
        if response.status_code == 200:
            print(f"Transmitted: {simulated_temp}°C | Server Response: {response.json().get('message')}")
        else:
            print(f"Failed to transmit. Server returned status code {response.status_code}: {response.text}")
            
        time.sleep(5)

except KeyboardInterrupt:
    print("\nIoT Simulation stopped by user.")