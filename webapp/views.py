from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
import requests
import json
import csv
import os
from utils.CurlWrapper import CurlWrapper
from utils.getThumbnailURL import extract_thumbnail
from utils.encodeQueryParameter import encode_query_parameter
from utils.extractSiteName import extract_site_name
from .forms import UserRegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def user_register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect if user is already logged in
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'webapp/register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect if user is already logged in
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                # Set access token as a cookie
                response = redirect('dashboard')
                response.set_cookie('access_token', access_token, httponly=False)

                # Store access token in the session
                request.session['access_token'] = access_token


                return response
            else:
                # Invalid credentials message
                error_message = "Invalid username or password"
                return render(request, 'webapp/login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()
    
    return render(request, 'webapp/login.html', {'form': form})

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')  # Redirect to login page after logout


def index(request):
    return render(request, 'webapp/index.html')


@login_required
def collections(request, name):
    collection_name = name
    api_url = f"http://localhost:8000/api/bookmarks/"

    # Extract query parameters from user's request
    # collection = request.GET.get('collection')
    sort_by = request.GET.get('sort_by', 'recent')  # Default to 'recent' if not provided

    # Append query parameters to the API URL
    name = encode_query_parameter(name)
    sort_by = encode_query_parameter(sort_by)
    api_url += f"?collection={name}&sort_by={sort_by}"

    curl_wrapper = CurlWrapper()
    jwt_token = request.session.get('access_token')
    headers = {'Authorization': "Bearer {}".format(jwt_token)}
    curl_response = curl_wrapper.get(api_url, headers=headers)

    context = {}
    status_code = curl_response.get('status_code')
    response_json = curl_response.get('response_json')

    print(context, name, api_url)

    if 200 <= status_code < 300 and response_json:
        context['bookmarks_list'] = response_json

        for bookmark in context['bookmarks_list']:
            bookmark['site_name'] = extract_site_name(bookmark['url'])
    elif status_code == 401:
        return redirect("http://localhost:8000/accounts/logout")
    
    listContext = getTagsAndCollectionList(request)
    context = {**context, **listContext}
    context['collection_name'] = collection_name
    context['type'] = "collection"

    return render(request, 'webapp/collections.html', context)


@login_required
def tags(request, name):
    tag_name = name
    api_url = f"http://localhost:8000/api/bookmarks/"

    # Extract query parameters from user's request
    # tag = request.GET.get('tag')
    sort_by = request.GET.get('sort_by', 'recent')  # Default to 'recent' if not provided

    # Append query parameters to the API URL
    name = encode_query_parameter(name)
    sort_by = encode_query_parameter(sort_by)

    api_url += f"?tag={name}&sort_by={sort_by}"

    curl_wrapper = CurlWrapper()
    jwt_token = request.session.get('access_token')
    headers = {'Authorization': "Bearer {}".format(jwt_token)}
    curl_response = curl_wrapper.get(api_url, headers=headers)

    context = {}
    status_code = curl_response.get('status_code')
    response_json = curl_response.get('response_json')

    if 200 <= status_code < 300 and response_json:
        context['bookmarks_list'] = response_json

        for bookmark in context['bookmarks_list']:
            bookmark['site_name'] = extract_site_name(bookmark['url'])
    elif status_code == 401:
        return redirect("http://localhost:8000/accounts/logout")
    
    listContext = getTagsAndCollectionList(request)
    context = {**context, **listContext}
    context['tag_name'] = tag_name
    context['type'] = "tag"

    return render(request, 'webapp/tags.html', context)

@login_required
def getTagsAndCollectionList(request):
    api_url = f"http://localhost:8000/api/tags/"
    api_url2 = f"http://localhost:8000/api/collections/"

    curl_wrapper = CurlWrapper()
    jwt_token = request.session.get('access_token')
    headers = {'Authorization': "Bearer {}".format(jwt_token)}
    curl_response = curl_wrapper.get(api_url, headers=headers)
    curl_response2 = curl_wrapper.get(api_url2, headers=headers)
    

    context = {}

    status_code = curl_response.get('status_code')
    response_json = curl_response.get('response_json')
    if 200 <= status_code < 300 and response_json:
        context['tags_list'] = response_json
    elif status_code == 401:
        return redirect("http://localhost:8000/accounts/logout")

    status_code2 = curl_response2.get('status_code')
    response_json2 = curl_response2.get('response_json')
    if 200 <= status_code2 < 300 and response_json2:
        context['collection_list'] = response_json2
    elif status_code == 401:
        return redirect("http://localhost:8000/accounts/logout")
    
    return context

@login_required
def dashboard(request):
    context = getTagsAndCollectionList(request)
    try :
        if context.status_code == 302:
            return context;
    except:
        pass
    
    return render(request, 'webapp/dashboard.html', context)


@login_required
def all_bookmarks(request):

    api_url = f"http://localhost:8000/api/bookmarks/"

    # Extract query parameters from user's request
    sort_by = request.GET.get('sort_by', 'recent')  # Default to 'recent' if not provided

    # Append query parameters to the API URL
    sort_by = encode_query_parameter(sort_by)
    api_url += f"?sort_by={sort_by}"

    curl_wrapper = CurlWrapper()
    
    jwt_token = request.session.get('access_token')
    headers = {'Authorization': "Bearer {}".format(jwt_token)}
    curl_response = curl_wrapper.get(api_url, headers=headers)
    
    context = {}
    status_code = curl_response.get('status_code')
    response_json = curl_response.get('response_json')

    if 200 <= status_code < 300 and response_json:
        context['bookmarks_list'] = response_json

        for bookmark in context['bookmarks_list']:
            bookmark['site_name'] = extract_site_name(bookmark['url'])
    elif status_code == 401:
        return redirect("http://localhost:8000/accounts/logout")

    listContext = getTagsAndCollectionList(request)
    context = {**context, **listContext}

    return render(request, 'webapp/all_bookmarks.html', context)



@login_required
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
    jwt_token = request.session.get('access_token')
    headers = {'Authorization': "Bearer {}".format(jwt_token)}
    curl_response = curl_wrapper.get(api_url, headers=headers)

    context = {}
    status_code = curl_response.get('status_code')
    response_json = curl_response.get('response_json')

    if 200 <= status_code < 300 and response_json:
        context['bookmarks_list'] = response_json

        for bookmark in context['bookmarks_list']:
            bookmark['site_name'] = extract_site_name(bookmark['url'])
    elif status_code == 401:
        return redirect("http://localhost:8000/accounts/logout")
    
    print("=====!====", curl_response)
    listContext = getTagsAndCollectionList(request)
    context = {**context, **listContext}

    return render(request, 'webapp/unsorted.html', context)


@login_required
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
    jwt_token = request.session.get('access_token')
    headers = {'Authorization': "Bearer {}".format(jwt_token)}
    curl_response = curl_wrapper.get(api_url, headers=headers)

    context = {}
    status_code = curl_response.get('status_code')
    response_json = curl_response.get('response_json')

    if 200 <= status_code < 300 and response_json:
        context['bookmarks_list'] = response_json

        for bookmark in context['bookmarks_list']:
            bookmark['site_name'] = extract_site_name(bookmark['url'])
    elif status_code == 401:
        return redirect("http://localhost:8000/accounts/logout")
    

    print("=====!====", curl_response)
    listContext = getTagsAndCollectionList(request)
    context = {**context, **listContext}

    return render(request, 'webapp/trash.html', context)


@login_required
def audios(request):
    return render(request, 'webapp/audios.html')

@login_required
def videos(request):
    return render(request, 'webapp/videos.html')

@login_required
def articles(request):
    return render(request, 'webapp/articles.html')

@login_required
def notes(request):
    return render(request, 'webapp/notes.html')

@login_required
def documents(request):
    return render(request, 'webapp/documents.html')

@login_required
def search(request):
    api_url = f"http://localhost:8000/api/search/"

    # Extract query parameters from user's request
    search = request.GET.get('query', '')  

    # Append query parameters to the API URL
    search = encode_query_parameter(search)
    api_url += f"?query={search}"

    curl_wrapper = CurlWrapper()
    
    jwt_token = request.session.get('access_token')
    headers = {'Authorization': "Bearer {}".format(jwt_token)}
    curl_response = curl_wrapper.get(api_url, headers=headers)
    
    context = {}
    status_code = curl_response.get('status_code')
    response_json = curl_response.get('response_json')

    if 200 <= status_code < 300 and response_json:
        context['bookmarks_list'] = response_json

        for bookmark in context['bookmarks_list']:
            bookmark['site_name'] = extract_site_name(bookmark['url'])
    elif status_code == 401:
        return redirect("http://localhost:8000/accounts/logout")

    listContext = getTagsAndCollectionList(request)
    context = {**context, **listContext}

    return render(request, 'webapp/search.html', context)


@login_required
def deleteBookmark(request,id):
    api_url = f"http://localhost:8000/api/bookmarks/{id}"
    curl_wrapper = CurlWrapper()
    jwt_token = request.session.get('access_token')
    headers = {'Authorization': "Bearer {}".format(jwt_token)}
    curl_response = curl_wrapper.delete(api_url, headers=headers)

    context = {}
    status_code = curl_response.get('status_code')
    response_json = curl_response.get('response_json')

    if 200 <= status_code < 300 and response_json:
        context['deleted'] = True
    elif status_code == 401:
        return redirect("http://localhost:8000/accounts/logout")
    
    referring_page = request.META.get('HTTP_REFERER')
    return redirect(referring_page)

@login_required
def restoreBookmark(request,id):
    api_url = f"http://localhost:8000/api/bookmarks/{id}"
    
    data = { "is_trash" : False }
    data = json.dumps(data)

    curl_wrapper = CurlWrapper()
    jwt_token = request.session.get('access_token')
    headers = {'Authorization': "Bearer {}".format(jwt_token), 'Content-Type': 'application/json'}
    curl_response = curl_wrapper.patch(api_url,  data=data, headers=headers)

    context = {}
    status_code = curl_response.get('status_code')
    response_json = curl_response.get('response_json')

    if 200 <= status_code < 300 and response_json:
        context['restored'] = True
    elif status_code == 401:
        return redirect("http://localhost:8000/accounts/logout")
    
    referring_page = request.META.get('HTTP_REFERER')
    return redirect(referring_page)


@login_required
def download_csv(request, type, identifier=None):

    api_url = f'http://localhost:8000/api/download/csv/{type}/{identifier}/'
    if (type == "all"):
        api_url = f'http://localhost:8000/api/download/csv/{type}/'
    
    jwt_token = request.session.get('access_token')
    headers = {'Authorization': "Bearer {}".format(jwt_token)}
    response = requests.get(api_url, headers=headers)


    if response.status_code == 200:
        if identifier:
            filename = "" + type + "_" + identifier + ".csv"
        else:
            filename = "all_bookmarks.csv"

        response = HttpResponse(response.content, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    else:
        return HttpResponse('Error while fetching CSV data', status=500)

@login_required
def download_file_from_url(request):
    if request.method == 'GET':
        try: 
            url = request.GET.get('url')  # Assuming the URL parameter is named 'url'
            filename = request.GET.get('filename')  # Assuming the URL parameter is named 'url'

            if url:
                response = requests.get(url)

                if response.status_code == 200:
                    content = response.content
                    filename = filename  # Get the filename from the URL
                    response = HttpResponse(content, content_type='application/octet-stream')
                    response['Content-Disposition'] = f'attachment; filename="{filename}"'
                    return response
                else:
                    return JsonResponse({ "error" : "Failed to download file from the given URL.", "status":400})
        except:
            return JsonResponse({ "error" : "An error occured while processing your request. File offline conversions might still working or internal server error !", "status":500})    
    return JsonResponse({"error":"Invalid request method.", "status":405})