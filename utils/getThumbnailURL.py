# from bs4 import BeautifulSoup
# import requests
# import time

# api_key = "c014ef5a9c94491ab1134f996aaaeb15"
# url = "https://pypi.org/project/beautifulsoup4/"

# def extract_thumbnail(url, api_key):
#     response = requests.get(url)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, 'html.parser')
        
#         # Try to find the OG image
#         og_image = soup.find('meta', property='og:image')
#         if og_image:
#             og_image_url = og_image['content']
#             # Upload the OG image to ImgBB and return the display URL
#             response = requests.post(
#                 "https://api.imgbb.com/1/upload",
#                 data={"key": api_key, "image": og_image_url}
#             )
#             if response.status_code == 200:
#                 imgbb_data = response.json()
#                 return imgbb_data['data']['display_url']
        
#         # If OG image is not available, find the first img tag in the HTML
#         img_tags = soup.find_all('img')
#         if img_tags:
#             first_img_src = img_tags[0].get('src')
#             if first_img_src:
#                 # Upload the image to ImgBB and return the display URL
#                 response = requests.post(
#                     "https://api.imgbb.com/1/upload",
#                     data={"key": api_key, "image": first_img_src}
#                 )
#                 if response.status_code == 200:
#                     imgbb_data = response.json()
#                     return imgbb_data['data']['display_url']
            
#     return 'xxxxxx'  # Replace with the URL of your default image/icon

# st = time.time()
# print(extract_thumbnail(url, api_key))
# et = time.time()
# print("Time :: "  + str(et - st))


from bs4 import BeautifulSoup
import json
import time
import subprocess
from urllib.parse import urlparse

url = "https://chat.openai.com/?model=text-davinci-002-render-sha"


def is_valid_url(input_string):
    try:
        result = urlparse(input_string)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def extract_thumbnail(url):
    try:
        command = ['curl', '-s', '-o', '-', '-w', '%{http_code}', '-L' ,url]
        output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        response_text = output.stdout.decode('utf-8', errors='replace')
        status_code = int(response_text[-3:])
        response_content = response_text[:-3]

        if status_code == 200:
            soup = BeautifulSoup(response_content, 'html.parser')

            # Try to find the OG image
            og_image = soup.find('meta', property='og:image')
            if og_image:
                og_image_url = og_image.get('content')
                print(og_image_url + "##########")
                if is_valid_url(og_image_url):
                    return og_image_url

            # If OG image is not available, find the first img tag in the HTML
            img_tags = soup.find_all('img')
            if img_tags:
                first_img_src = img_tags[0].get('src')
                if is_valid_url(first_img_src):
                    return first_img_src

    except Exception as e:
        pass  # Suppress the exception and proceed with default value

    return 'https://i.ibb.co/3RLm4Jc/629a49e7ab53625cb2c4e791-Brand-pattern.jpg'

st = time.time()
print(extract_thumbnail(url))
et = time.time()
print("Time:", et - st)
# extract_thumbnail("https://chat.openai.com/?model=text-davinci-002-render-sha")