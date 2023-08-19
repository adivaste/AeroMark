from django.shortcuts import render
import requests
import time
import json
from utils.CurlWrapper import CurlWrapper
from utils.getThumbnailURL import extract_thumbnail
from utils.encodeQueryParameter import encode_query_parameter
from django.shortcuts import redirect
from utils.extractSiteName import extract_site_name


def index(request):
    return render(request, 'webapp/index.html')

def collections(request, name):
    api_url = f"http://localhost:8000/api/bookmarks/"

    # Extract query parameters from user's request
    # collection = request.GET.get('collection')
    sort_by = request.GET.get('sort_by', 'recent')  # Default to 'recent' if not provided

    # Append query parameters to the API URL
    name = encode_query_parameter(name)
    sort_by = encode_query_parameter(sort_by)
    api_url += f"?collection={name}&sort_by={sort_by}"

    curl_wrapper = CurlWrapper()
    curl_response = curl_wrapper.get(api_url)

    context = {}
    status_code = curl_response.get('status_code')
    response_json = curl_response.get('response_json')

    if 200 <= status_code < 300 and response_json:
        context['bookmarks_list'] = response_json

        for bookmark in context['bookmarks_list']:
            bookmark['site_name'] = extract_site_name(bookmark['url'])

    listContext = getTagsAndCollectionList()
    context = {**context, **listContext}

    return render(request, 'webapp/collections.html', context)


def tags(request, name):
    api_url = f"http://localhost:8000/api/bookmarks/"

    # Extract query parameters from user's request
    # tag = request.GET.get('tag')
    sort_by = request.GET.get('sort_by', 'recent')  # Default to 'recent' if not provided

    # Append query parameters to the API URL
    name = encode_query_parameter(name)
    sort_by = encode_query_parameter(sort_by)

    api_url += f"?tag={name}&sort_by={sort_by}"

    curl_wrapper = CurlWrapper()
    curl_response = curl_wrapper.get(api_url)

    context = {}
    status_code = curl_response.get('status_code')
    response_json = curl_response.get('response_json')

    if 200 <= status_code < 300 and response_json:
        context['bookmarks_list'] = response_json

        for bookmark in context['bookmarks_list']:
            bookmark['site_name'] = extract_site_name(bookmark['url'])
            
    listContext = getTagsAndCollectionList()
    context = {**context, **listContext}

    return render(request, 'webapp/tags.html', context)


def getTagsAndCollectionList():
    api_url = f"http://localhost:8000/api/tags/"
    api_url2 = f"http://localhost:8000/api/collections/"

    curl_wrapper = CurlWrapper()
    curl_response = curl_wrapper.get(api_url)
    curl_response2 = curl_wrapper.get(api_url2)

    context = {}

    status_code = curl_response.get('status_code')
    response_json = curl_response.get('response_json')
    if 200 <= status_code < 300 and response_json:
        context['tags_list'] = response_json

    status_code2 = curl_response2.get('status_code')
    response_json2 = curl_response2.get('response_json')
    if 200 <= status_code2 < 300 and response_json2:
        context['collection_list'] = response_json2
    
    return context

def dashboard(request):
    context = getTagsAndCollectionList()
    return render(request, 'webapp/dashboard.html', context)

def all_bookmarks(request):
    api_url = f"http://localhost:8000/api/bookmarks/"

    # Extract query parameters from user's request
    sort_by = request.GET.get('sort_by', 'recent')  # Default to 'recent' if not provided

    # Append query parameters to the API URL
    sort_by = encode_query_parameter(sort_by)
    api_url += f"?sort_by={sort_by}"

    curl_wrapper = CurlWrapper()
    curl_response = curl_wrapper.get(api_url)

    context = {}
    status_code = curl_response.get('status_code')
    response_json = curl_response.get('response_json')

    if 200 <= status_code < 300 and response_json:
        context['bookmarks_list'] = response_json

        for bookmark in context['bookmarks_list']:
            bookmark['site_name'] = extract_site_name(bookmark['url'])

    listContext = getTagsAndCollectionList()
    context = {**context, **listContext}

    return render(request, 'webapp/all_bookmarks.html', context)


def unsorted(request):
    api_url = f"http://localhost:8000/api/bookmarks/"

    # Extract query parameters from user's request
    collection_name = "No Collection"
    sort_by = request.GET.get('sort_by', 'recent')  # Default to 'recent' if not provided

    # Append query parameters to the API URL
    collection_name = encode_query_parameter(collection_name)
    sort_by = encode_query_parameter(sort_by)
    api_url += f"?collection={collection_name}&sort_by={sort_by}"

    curl_wrapper = CurlWrapper()
    curl_response = curl_wrapper.get(api_url)

    context = {}
    status_code = curl_response.get('status_code')
    response_json = curl_response.get('response_json')

    if 200 <= status_code < 300 and response_json:
        context['bookmarks_list'] = response_json

        for bookmark in context['bookmarks_list']:
            bookmark['site_name'] = extract_site_name(bookmark['url'])

    print("=====!====", curl_response)
    listContext = getTagsAndCollectionList()
    context = {**context, **listContext}

    return render(request, 'webapp/unsorted.html', context)

def trash(request):
    api_url = f"http://localhost:8000/api/bookmarks/"

    # Extract query parameters from user's request
    is_trash = "True"
    sort_by = request.GET.get('sort_by', 'recent')  # Default to 'recent' if not provided

    # Append query parameters to the API URL
    is_trash = encode_query_parameter(is_trash)
    sort_by = encode_query_parameter(sort_by)
    api_url += f"?trash={is_trash}&sort_by={sort_by}"

    curl_wrapper = CurlWrapper()
    curl_response = curl_wrapper.get(api_url)

    context = {}
    status_code = curl_response.get('status_code')
    response_json = curl_response.get('response_json')

    if 200 <= status_code < 300 and response_json:
        context['bookmarks_list'] = response_json

        for bookmark in context['bookmarks_list']:
            bookmark['site_name'] = extract_site_name(bookmark['url'])

    print("=====!====", curl_response)
    listContext = getTagsAndCollectionList()
    context = {**context, **listContext}

    return render(request, 'webapp/trash.html', context)

def audios(request):
    return render(request, 'webapp/audios.html')

def videos(request):
    return render(request, 'webapp/videos.html')

def articles(request):
    return render(request, 'webapp/articles.html')

def notes(request):
    return render(request, 'webapp/notes.html')

def documents(request):
    return render(request, 'webapp/documents.html')

def login(request):
    return render(request, 'webapp/login.html')

def register(request):
    return render(request, 'webapp/register.html')


def deleteBookmark(request,id):
    api_url = f"http://localhost:8000/api/bookmarks/{id}"
    curl_wrapper = CurlWrapper()
    curl_response = curl_wrapper.delete(api_url)

    context = {}
    status_code = curl_response.get('status_code')
    response_json = curl_response.get('response_json')

    if 200 <= status_code < 300 and response_json:
        context['deleted'] = True

    referring_page = request.META.get('HTTP_REFERER')
    return redirect(referring_page)

def restoreBookmark(request,id):
    api_url = f"http://localhost:8000/api/bookmarks/{id}"
    
    data = { "is_trash" : False }
    data = json.dumps(data)
    headers={'Content-Type': 'application/json'}

    curl_wrapper = CurlWrapper()
    curl_response = curl_wrapper.patch(api_url, data=data, headers=headers)

    context = {}
    status_code = curl_response.get('status_code')
    response_json = curl_response.get('response_json')

    if 200 <= status_code < 300 and response_json:
        context['restored'] = True

    referring_page = request.META.get('HTTP_REFERER')
    return redirect(referring_page)

