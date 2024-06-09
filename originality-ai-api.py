# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 15:41:11 2024

@author: mhayes
"""

# -*- coding: utf-8 -*-
"""
Created on Fri May 31 15:25:19 2024

@author: mhayes
"""
import json
import requests
import datetime
import time

# Replace with your actual API key
API_KEY = ''
BASE_URL = 'https://api.originality.ai/api/v1/'


def word_count(s):
    words = s.split()
    return len(words)

def truncate_to_3000_words(s):
    # Split the string into words
    words = s.split()
    
    # Check if the word count is greater than 3000
    if len(words) > 3000:
        # Slice the list to keep only the first 3000 words
        truncated_words = words[:2900]
        
        # Join the words back into a single string
        truncated_string = ' '.join(truncated_words)
    else:
        # If the word count is less than or equal to 3000, return the original string
        truncated_string = s
    
    return truncated_string

def check_plagiarism(text, excluded_url = ''):
    endpoint = 'scan/ai-plag'
    url = BASE_URL + endpoint
    
    headers = {
        'Accept' : 'application/json',
        'X-OAI-API-KEY': f'{API_KEY}',
        'Content-Type': 'application/json',
        'user-agent': 'Mozilla'
    }
    
    payload = json.dumps({
        'content': text,
        'excludedUrl': excluded_url,
        "aiModelVersion": 1
    })
    
    response = requests.post(url, headers=headers, data=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(response.json())

#check_articles takes a list of dictionaries, 
def check_articles(article_list, api_limit = 100, json_filename = 'article_list'):
    # Example usage
    i = 0
    total_credits_used = 0     
    
    for guide in article_list:
        #if i >= api_limit or guide.get('plag','') != '':
        #    continue
        if guide.get("plag") and not guide.get("plag").get("ai"):
            i+=1
            text_to_check = guide.get("content").get("stripped","")
            if word_count(text_to_check) >= 3000:
                text_to_check = truncate_to_3000_words(text_to_check)
            if text_to_check != '':
                result = check_plagiarism(text_to_check)
                if result is not None:
                    guide["plag"] = result
                    total_credits_used += result.get("credits_used", 0)
                    i += 1
                    
                    if i%50 == 0:
                    # create a datetime object with the current date and time
                        now = datetime.datetime.now()
            
                        # format the datetime as a string with a specific format
                        timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")
        
                            
                        with open(json_filename + timestamp + '.json', 'w') as f:
                            # Convert the dictionary to a JSON string and write it to the file
                            json.dump(article_list, f)
        
                else:
                    print("No results")
    
    return {"results": article_list, "total_credits_used": total_credits_used}
    
    
    
