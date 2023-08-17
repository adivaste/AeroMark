# import subprocess
# import time

# class CurlWrapper:
#     def __init__(self):
#         pass

#     def _execute_curl(self, url, method, headers=None, data=None):
#         command = ['curl', '-X', method, url]

#         if headers:
#             for key, value in headers.items():
#                 command.extend(['-H', f'{key}: {value}'])

#         if data:
#             command.extend(['--data', data])

#         try:
#             result = subprocess.run(command, capture_output=True, text=True, check=True)
            
#             response = {
#                 'status_code': result.returncode,
#                 'text': result.stdout,
#                 'error': result.stderr
#             }
            
#             return response
#         except subprocess.CalledProcessError as e:
#             response = {
#                 'status_code': e.returncode,
#                 'error': e.stderr
#             }
            
#             return response

#     def get(self, url, headers=None):
#         return self._execute_curl(url, method='GET', headers=headers)

#     def post(self, url, data=None, headers=None):
#         return self._execute_curl(url, method='POST', headers=headers, data=data)

#     def put(self, url, data=None, headers=None):
#         return self._execute_curl(url, method='PUT', headers=headers, data=data)

#     def delete(self, url, headers=None):
#         return self._execute_curl(url, method='DELETE', headers=headers)

import subprocess
import json

class CurlWrapper:
    def __init__(self):
        pass

    def _execute_curl(self, url, method, headers=None, data=None):
        command = ['curl', '-s', '-o', '-', '-w', '%{http_code}', '-X', method, url]

        if headers:
            for key, value in headers.items():
                command.extend(['-H', f'{key}: {value}'])

        if data:
            command.extend(['--data', data])

        try:
            print(command)
            output = subprocess.run(command, capture_output=True, text=True, check=True)
            status_code = int(output.stdout[-3:])
            response = output.stdout[:-3]

            response_dict = {
                'status_code': status_code,
                'response': response
            }

            try:
                response_json = json.loads(response)
                response_dict['response_json'] = response_json
            except json.JSONDecodeError:
                pass

            return response_dict
        except subprocess.CalledProcessError as e:
            error_response = {
                'status_code': e.returncode,
                'error': e.stderr
            }
            
            return error_response

    def get(self, url, headers=None):
        return self._execute_curl(url, method='GET', headers=headers)

    def post(self, url, data=None, headers=None):
        return self._execute_curl(url, method='POST', headers=headers, data=data)

    def put(self, url, data=None, headers=None):
        return self._execute_curl(url, method='PUT', headers=headers, data=data)
    
    def patch(self, url, data=None, headers=None):
        return self._execute_curl(url, method='PATCH', headers=headers, data=data)

    def delete(self, url, headers=None):
        return self._execute_curl(url, method='DELETE', headers=headers)
