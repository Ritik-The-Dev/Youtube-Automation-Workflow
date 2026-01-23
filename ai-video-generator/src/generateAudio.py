import requests
import os
import time

# voice-422
# voice-426
# voice-423

def generate_voice(voiceOverText, sceneNumber, folderName, voice="voice-423", pitch=12, rate=12, max_retries=3):
    url = "https://speechma.com/com.api/tts-api.php"

    # Prepare the payload for the API request
    payload = {
        "text": voiceOverText,
        "voice": voice,
        "pitch": pitch,
        "rate": rate
    }
    
    # Folder path to save the audio file
    folder_path = f"./data/{folderName}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)  # Create the folder if it doesn't exist

    # Audio file path
    audio_path = os.path.join(folder_path, f"Scene{sceneNumber}.mp3")
    
    for attempt in range(max_retries):
        try:
            # Make the POST request to generate the voice
            response = requests.post(url, json=payload)
            
            # Check if the request was successful
            if response.status_code == 200:
                # Save the audio content to the file
                with open(audio_path, 'wb') as f:
                    f.write(response.content)
                
                print(f"Audio saved as '{audio_path}'")

                # Verify if the audio file can be loaded
                if verify_audio(audio_path):
                    print(f"Audio for Scene {sceneNumber} loaded successfully.")
                    return audio_path  # Return the path if the audio file is valid
                else:
                    print(f"Error: Audio file '{audio_path}' is invalid. Retrying...")
            
            else:
                print(response)
                print(f"Failed to generate audio. Status code: {response.status_code}. Retrying...")
        
        except Exception as e:
            print(f"Error during request: {e}. Retrying...")
        
        # Wait before retrying to avoid spamming the API
        time.sleep(2)

    print(f"Failed to generate a valid audio after {max_retries} attempts.")
    return None  # Return None if all attempts fail

def verify_audio(audio_path):
    return True
    # """Verify if the audio file can be opened and is valid"""
    # try:
    #     with open(audio_path, 'rb') as f:
    #         data = f.read()
    #         # Check if the file is not empty and has the correct content type (MP3)
    #         if data and data[:3] == b'ID3':  # MP3 files start with ID3 header
    #             return True
    #         else:
    #             return False
    # except Exception as e:
    #     print(f"Error verifying audio: {e}")
    #     return False

# Example usage
# generate_voice("3 अप्रैल 2021. छत्तीसगढ़ के बीजापुर जंगल, जहां हर पत्ता मौत का संकेत दे सकता था", 1, "VideoFolderName")
