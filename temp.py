# import pdfkit

# pdfkit.from_url('https://stackoverflow.com/questions/23359083/how-to-convert-webpage-into-pdf-by-using-python', 'out.pdf')

# from pyhtml2pdf import converter

# converter.convert('https://pypi.org', 'sample.pdf')

# import weasyprint
# pdf = weasyprint.HTML('http://www.google.com').write_pdf()
# len(pdf)
# open('google.pdf', 'wb').write(pdf)

# -======================================================
# import subprocess
# import json

# class CurlWrapper:
#     def __init__(self):
#         pass

#     def _execute_curl(self, url, method, headers=None, data=None):
#         command = ['curl', '-s', '-o', '-', '-w', '%{http_code}', '-X', method, url]

#         if headers:
#             for key, value in headers.items():
#                 command.extend(['-H', f'{key}: {value}'])

#         if data:
#             command.extend(['--data', data])

#         try:
#             output = subprocess.run(command, capture_output=True, text=True, check=True)
#             status_code = int(output.stdout[-3:])
#             response = output.stdout[:-3]

#             response_dict = {
#                 'status_code': status_code,
#                 'response': response
#             }

#             try:
#                 response_json = json.loads(response)
#                 response_dict['response_json'] = response_json
#             except json.JSONDecodeError:
#                 pass

#             return response_dict
#         except subprocess.CalledProcessError as e:
#             error_response = {
#                 'status_code': e.returncode,
#                 'error': e.stderr
#             }
            
#             return error_response

#     def get(self, url, headers=None):
#         return self._execute_curl(url, method='GET', headers=headers)

#     def post(self, url, data=None, headers=None):
#         return self._execute_curl(url, method='POST', headers=headers, data=data)

#     def put(self, url, data=None, headers=None):
#         return self._execute_curl(url, method='PUT', headers=headers, data=data)

#     def delete(self, url, headers=None):
#         return self._execute_curl(url, method='DELETE', headers=headers)

# # temp = CurlWrapper()
# # url = "http://localhost:8000/api/tags/"
# # res = temp.get(url)
# # print(res)

# import requests

# data = {
#     "username" : "rohit",
#     "password"  : "Pass@123"
# }

# response = requests.post("http://localhost:8000/api/token/", data=data)
# print(response)
# print(response.text)
# print(response.status_code)

# import asyncio

# async def async_function():
#     print("Async function started")
#     await asyncio.sleep(2)
#     print("Async function completed")

# async def main():
#     print("Main function started")
#     asyncio.create_task(async_function())  # Start async function concurrently
#     print("Main function completed")
#     await asyncio.sleep(6)

# # Run the event loop to execute asynchronous functions
# asyncio.run(main())

import threading
import time

# Simulating bookmark conversion to PDF and taking a screenshot
def convert_to_pdf(bookmark):
    time.sleep(5)  # Simulate PDF conversion
    print(f"Converting bookmark '{bookmark}' to PDF...")
    print(f"Bookmark '{bookmark}' converted to PDF")

def take_screenshot(bookmark):
    time.sleep(3)  # Simulate taking a screenshot
    print(f"Taking screenshot of bookmark '{bookmark}'...")
    print(f"Screenshot taken for bookmark '{bookmark}'")

# Function to handle the user request
def handle_request(bookmark):
    print(f"Handling request for bookmark '{bookmark}'")
    pdf_thread = threading.Thread(target=convert_to_pdf, args=(bookmark,))
    screenshot_thread = threading.Thread(target=take_screenshot, args=(bookmark,))
    pdf_thread.start()  # Start PDF conversion thread
    screenshot_thread.start()  # Start screenshot thread
    return f"Request for bookmark '{bookmark}' received and tasks initiated."

def main():
    bookmark = "example.com"
    response = handle_request(bookmark)
    print(response)

if __name__ == "__main__":
    main()
