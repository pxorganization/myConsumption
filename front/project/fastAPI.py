from fastapi import FastAPI
from fastapi.responses import FileResponse
import sys
import os

# Add the path to the 'back' directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../back')))

# Now you can import from diagramMat.py
from diagramMat import main

app = FastAPI()

# Define static image path
STATIC_FOLDER = "C:/Users/koron/OneDrive/Traffic LightWave/Hackathons/Ai Hackathon (ACEin)/back/static"
IMAGE_PATH = os.path.join(STATIC_FOLDER, "bar_chart.png")

# Ensure static folder exists
os.makedirs(STATIC_FOLDER, exist_ok=True)

plt, fig = main()

def save_plot(plt, fig):
    # Saving
    plt.savefig(IMAGE_PATH)
    plt.close(fig)
    print(f"✅ Chart saved at: {IMAGE_PATH}")

save_plot(plt, fig)

@app.get("/image")
def get_image():
    """ Serve the generated image. """
    if os.path.exists(IMAGE_PATH):
        return FileResponse(IMAGE_PATH)
    return {"error": "Image not found"}



# Run with: uvicorn fastAPI:app --reload
