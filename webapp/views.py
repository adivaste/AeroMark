from django.shortcuts import render
import requests
import time
import json
from utils.CurlWrapper import CurlWrapper
from utils.getThumbnailURL import extract_thumbnail
from django.shortcuts import redirect
from utils.extractSiteName import extract_site_name


def index(request):
    return render(request, 'webapp/index.html')

def collections(request, id):
    api_url = f"http://localhost:8000/api/collections/{id}"
    curl_wrapper = CurlWrapper()
    curl_response = curl_wrapper.get(api_url)

    context = {}
    status_code = curl_response.get('status_code')
    response_json = curl_response.get('response_json')

    if 200 <= status_code < 300 and response_json:
        context['collection_info'] = response_json
    return render(request, 'webapp/collections.html', context)


def tags(request, id):
    return render(request, 'webapp/tags.html')

def dashboard(request):
    return render(request, 'webapp/dashboard.html')

def all_bookmarks(request):
    api_url = f"http://localhost:8000/api/bookmarks/"
    curl_wrapper = CurlWrapper()
    curl_response = curl_wrapper.get(api_url)

    context = {}
    status_code = curl_response.get('status_code')
    response_json = curl_response.get('response_json')

    if 200 <= status_code < 300 and response_json:
        context['bookmarks_list'] = response_json

        for bookmark in context['bookmarks_list']:
            bookmark['site_name'] = extract_site_name(bookmark['url'])

    return render(request, 'webapp/all_bookmarks.html', context)

def unsorted(request):
    return render(request, 'webapp/unsorted.html')

def trash(request):
    return render(request, 'webapp/trash.html')

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

