import filestack

def upload_file_and_get_url(file_path):
    try:
        api_key = 'Au3QJNlTjRie7ynfCrgz5z'
        client = filestack.Client(api_key)
        response = client.upload(filepath=file_path)
        uploaded_url = response.url
        
        return {'success': True, 'url': uploaded_url}
    except Exception as e:
        return {'success': False, 'error': str(e)}

if __name__ == "__main__":
    file_path = 'screenshot1.png'  
    upload_result = upload_file_and_get_url(api_key, file_path)
    
    if upload_result['success']:
        print(f"File uploaded successfully. URL: {upload_result['uploaded_url']}")
    else:
        print(f"Upload failed. Error: {upload_result['error']}")
