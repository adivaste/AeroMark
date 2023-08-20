from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render
import requests
import time
import json
from utils.CurlWrapper import CurlWrapper
from utils.getThumbnailURL import extract_thumbnail
from utils.encodeQueryParameter import encode_query_parameter
from django.shortcuts import redirect
from utils.extractSiteName import extract_site_name
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, LoginForm
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

    listContext = getTagsAndCollectionList(request)
    context = {**context, **listContext}

    return render(request, 'webapp/collections.html', context)


@login_required
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
            
    listContext = getTagsAndCollectionList(request)
    context = {**context, **listContext}

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

    status_code2 = curl_response2.get('status_code')
    response_json2 = curl_response2.get('response_json')
    if 200 <= status_code2 < 300 and response_json2:
        context['collection_list'] = response_json2
    
    return context

@login_required
def dashboard(request):
    context = getTagsAndCollectionList(request)
    return render(request, 'webapp/dashboard.html', context)


@login_required
def all_bookmarks(request):

    # jwt_token2 = request.cookie.get('access_token')
    # print(jwt_token)
    print("HIIII")


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

    referring_page = request.META.get('HTTP_REFERER')
    return redirect(referring_page)

