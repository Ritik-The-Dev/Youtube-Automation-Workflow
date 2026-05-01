import os
import json
from src.script_writer import generate_with_feedback , save_generated_topic
from src.generateImage import generate_image
from src.generateAudio import generate_voice
from src.generateVideo import generate_video

def run():
    scene_data = generate_with_feedback()
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(BASE_DIR, "data", "File_To_Upload")
    os.makedirs(folder_path, exist_ok=True)
    
    scriptPath = os.path.join(folder_path, "Script.json")
    with open(scriptPath, 'w', encoding="utf-8") as f:
            json.dump(scene_data, f, ensure_ascii=False, indent=4)
    
    print("Scene generated successfully")
    
    for i in range(len(scene_data['scenes'])):
        voice = scene_data['scenes'][i]['voiceoverText']
        prompt = scene_data['scenes'][i]['imagePrompt']
        generate_image(prompt, i, "File_To_Upload")  
        generate_voice(voice, i, "File_To_Upload")  
    
    generate_video("File_To_Upload", scene_data, folder_path)
    save_generated_topic(scene_data["foodItem"])


if __name__ == "__main__":
    run()
