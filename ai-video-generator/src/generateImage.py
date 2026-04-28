import http.client
import urllib.parse
import os
from PIL import Image

conn = http.client.HTTPSConnection("gen.pollinations.ai")
headers = {
    "Authorization": "Bearer " + os.getenv("POLLINATIONS_API_KEY"),
}

def generate_image(prompt, sceneNumber, folderName, max_retries=3):
    encoded_request = urllib.parse.quote(prompt)
    modelNames = ['grok-imagine' ,'zimage','flux','gptimage']
    for attempt in range(max_retries):
        conn.request("GET", f"/image/{encoded_request}?model={modelNames[attempt]}&width=1080&height=1920", headers=headers)
        res = conn.getresponse()
        data = res.read()
        
        folder_path = f"./data/{folderName}"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        image_path = os.path.join(folder_path, f"Image{sceneNumber}.png")
        with open(image_path, 'wb') as f:
            f.write(data)

        print(f"Image saved as '{image_path}'")

        # Check if the image can be loaded correctly
        try:
            with Image.open(image_path) as img:
                img.verify()  
            print(f"Image '{image_path}' loaded successfully.")
            return image_path 
        except (IOError, SyntaxError) as e:
            print(f"Error loading image with model {modelNames[attempt]} : {e}")
            print(f"Retrying image generation with model {modelNames[attempt + 1]} ... (Attempt {attempt + 1} of {max_retries})")
            if attempt == max_retries - 1:
                print(f"Failed to generate a valid image after {max_retries} attempts.")
                return None 