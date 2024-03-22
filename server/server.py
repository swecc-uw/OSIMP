import os
import json
import threading
from datetime import datetime
from fastapi import FastAPI
import dotenv
import uvicorn
from job import main

# Global variables to store status and result
status = "waiting"
result = None
timestamp = None

# Function to simulate script execution
def run_script():
    global status
    global result
    global timestamp

    pairings, unpaired = main()

    # delete old files
    try:
        os.remove('cache/pairings.json')
    except:
        pass

    try:
        os.remove('cache/unpaired.json')
    except:
        pass

    # save to file
    with open('cache/pairings.json', 'w') as f:
        json.dump(pairings, f, default=lambda x: x.__dict__)

    with open('cache/unpaired.json', 'w') as f:
        json.dump(unpaired, f, default=lambda x: x.__dict__)

    # After completion, update status and result
    status = "finished"
    result = "Script execution completed successfully"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# FastAPI app instance
app = FastAPI()

# Load environment variables
dotenv.load_dotenv()

SCRIPT_SECRET = os.getenv("SCRIPT_SECRET")

# FastAPI route to handle script execution
@app.get("/execute-script")
def execute_script(secret: str):
    global status

    print(secret, SCRIPT_SECRET)
    # Check if the secret is correct
    if secret != SCRIPT_SECRET:
        return {"message": "Unauthorized"}

    if status == "running":
        return {"message": "Script already running"}

    # Set status to running
    status = "running"

    # Run the script in a separate thread
    thread = threading.Thread(target=run_script)
    thread.start()

    return {"message": "Script execution started"}

@app.get("/status")
def get_status():
    return {"status": status, "timestamp": timestamp}

@app.get("/pairs")
def get_pairs():
    try:
        with open('cache/pairings.json', 'r') as f:
            pairings = json.load(f)
        return {"pairings": pairings, "timestamp": timestamp}
    except:
        return {"message": "cache miss, execute script first"}

@app.get("/unpaired")
def get_unpaired():
    try:
        with open('cache/unpaired.json', 'r') as f:
            unpaired = json.load(f)
        return {"unpaired": unpaired, "timestamp": timestamp}
    except:
        return {"message": "cache miss, execute script first"}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
