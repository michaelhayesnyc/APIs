# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 15:58:19 2024

@author: mhayes

@description: Interacts with the OpenAI API, constructs prompts (including images), collects responses, stores in JSON files periodically.
"""

import json  # Assuming the use of json for simplicity in this example
import openai
import base64
import requests
import datetime
import time

#API Key - Replace with your Key
api_key=""

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}   

#Filenames for backing up the JSON Data.  Add your specific paths/filenames as necessary
file_names = ['data-1.json','data-2.json','data-3.json','data-4.json','data-5.json']
file_index = 0
api_limit = 100000
i = 0

#Encode an image file to base64 from the local filesystem.
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

#Encode an image file to base64 from a URL.
def encode_image_from_url(url):
    try:
        # Download the image
        print(f"Trying URL: {url}")
        response = requests.get(url, headers = {'User-agent':'Mozilla'})
        # Check if the request was successful
        if response.status_code == 200:
            # Read the image data
            image_data = response.content
            # Encode the image data to base64
            encoded_image = base64.b64encode(image_data)
            # Convert bytes to string
            encoded_image_str = encoded_image.decode('utf-8')
            return encoded_image_str
        else:
            print("Failed to download image. Status code:", response.status_code)
            return None
    except Exception as e:
        print("An error occurred:", str(e))
        return None

#Modify to construct your own prompt.  This asks to summarize a series of data points, such as this:
    
# data_points = [
#     {"Date Point 1": "Fact 1"},
#     {"Other Data": "Other Fact"},
#     {"Yet More Data": "Yet another fact to summarize."}
# ]



def construct_prompt(data_points):
    prompt = json.dumps(data_points)
    prompt += " Summarize the above facts in a concise paragraph. Speak in formal tone."
    return prompt




for key, data in json_data.items():
    if data.get("skip") == True:
        continue
    else:
    
        print(f"Trying {key}")
        i += 1
        try:
    
            image_base64 = encode_image_from_url(data.get['imageLink'])
        except FileNotFoundError:
            print("File not found error, skipping")
            continue
        
        if image_base64 is None:
            continue
    
        prompt = construct_prompt(data.get("prompt_data"))
        
        payload = {
            "model": "gpt-4o",
            "max_tokens": 2000,
            "messages": [
                #{"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": [{"type":"text","text":prompt},
                                {"type": "image_url",
                                 "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                                 }]
                    
                }
            ]
        }
        
        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(payload), timeout = 120)
            response_json = response.json()
            
            data["description_chatgpt4_vision"] = response_json['choices'][0]['message']['content']
            data["chatgpt4-vision-generated"] = True
            time.sleep(5)
        except Exception as e:
            print(f"Error processing {key}: {e}")
            time.sleep(5)
            continue
        if i%40 == 0:
            with open(file_names[file_index], 'w') as f:
                json.dump(json_data, f)
                
            file_index = (file_index + 1) % len(file_names)
        

            
