# ===================================================
# === Import required modules and fucntions      ====
# ===================================================



from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.models import Bookmark, Tag, Collection
from api.serializers import BookmarkSerializer, TagSerializer, CollectionSerializer
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.conf import settings
from utils.getThumbnailURL import extract_thumbnail
from django.db.models import Q
import time
import jwt
import csv



# ===================================================
# === Get list of boookmarks ||  METHODS :: GET, POST
# ===================================================
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def bookmarks_list(request):
     
     # ==== Retrieve User ID from a Token ====
     extract_response = extract_user_id_from_jwt(request)
     if "user_id" not in extract_response:
         return Response({ "error" : extract_response.get("error")})
     user_id = extract_response.get("user_id")
     request.data["user"] = user_id


     # ==== If requested method is GET ====
     if request.method == 'GET':

        # ==== Check that perticular TAG | COLLECTION | TRASH | ORDER is requested or not ====
        # ==== Store the default values ====
        tag = None
        collection = None
        sort_by = 'recent'
        trash = False

        # ==== Data to return back ====
        data = None


        # ==== Check for SORT BY ====
        try:
            req_sort_by = request.query_params.get('sort_by')
            sort_possible_options = ['site_az', 'site_za', 'title_az', 'title_za', 'recent', 'older']
            if req_sort_by in sort_possible_options:
                sort_by = req_sort_by
        except:
             pass

        # ==== Check for COLLECTION | TAG | TRASH ====
        try: 
            req_collection = request.query_params.get('collection')
            req_tag = request.query_params.get('tag')
            req_trash = request.query_params.get('trash')

            # Check for trash
            if req_trash == "True" or req_trash == True:
                trash = True

            # Check for collection
            if req_collection:
                collection = req_collection

            # Check for tags
            elif not collection and req_tag:
                tag = req_tag
        except:
             pass
        

        # ==== Decide what data to send ====
        if trash:
            data = Bookmark.objects.filter(is_trash=True, user_id=user_id)
        else:
            if tag:
                data = Bookmark.objects.filter(tags__name=str(tag), is_trash=False, user_id=user_id)
            elif collection:
                data = Bookmark.objects.filter(collection__name=str(collection), is_trash=False, user_id=user_id)
            else:
                data = Bookmark.objects.filter(is_trash=False, user_id=user_id)


        # ==== Deciding sorting order ====
        if sort_by == 'site_az':
            data = data.order_by('url')
        elif sort_by == 'site_za':
            data = data.order_by('-url')
        elif sort_by == 'title_az':
            data = data.order_by('title')
        elif sort_by == 'title_za':
            data = data.order_by('-title')
        elif sort_by == 'recent':
            data = data.order_by('-created_at')
        elif sort_by == 'older':
            data = data.order_by('created_at')

        serializer = BookmarkSerializer(data, many=True)
        return Response(serializer.data)
     
     elif request.method == 'POST':

            # ==== Retrieve User ID from a Token ====
            extract_response = extract_user_id_from_jwt(request)
            if "user_id" not in extract_response:
                return Response({ "error" : extract_response.get("error")})
            user_id = extract_response.get("user_id")
            request.data["user"] = user_id

            print(user_id)

            # ==== Handles the tags, create and get instances ====
            userInstance = User.objects.get(id=user_id)
            tags = request.data.pop('tags', [])
            tag_instances = []
            for tag_name in tags:
                tag_serializer = TagSerializer(data={'name': tag_name, 'user': user_id})
                if tag_serializer.is_valid():
                    tag_instance, _ = Tag.objects.get_or_create(name=tag_name, user=userInstance)
                    tag_instances.append(tag_instance)
                else:
                    print(tag_serializer.errors)
                    return Response(tag_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            request.data['tags'] = [tag.id for tag in tag_instances]  # Convert tags to a list of tag IDs


            # ===== Getting collection instances or create it ====
            collection_name = request.data.get('collection')  
            if collection_name :
                  collection, _ = Collection.objects.get_or_create(name=collection_name, user=userInstance)
            else:
                  collection, _ = Collection.objects.get_or_create(name="No Collection", user=userInstance)

            request.data["collection"]=collection.id


            # ==== Creating thumbnail from URL ====
            try:
                 url = extract_thumbnail(request.data["url"])
                 request.data["thumbnail_url"] = url
                 print(request.data["thumbnail_url"] + "---" + request.data["url"])
            except:
                 pass
            

            # ==== Creating the object of BOOKMARK ====
            serializer = BookmarkSerializer(data=request.data)
            if serializer.is_valid():
                  bookmark = serializer.save()
                  serialized_data = serializer.to_representation(bookmark)  # Get the default serialized data

                  return Response(serialized_data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =========================================================
# === Operations on each bookmark ||  METHODS :: GET, POST
# =========================================================

@api_view(["GET","PATCH", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def bookmarks_detail(request, pk):
      
      extract_response = extract_user_id_from_jwt(request)
      if "user_id" not in extract_response:
        return Response({ "error" : extract_response.get("error")})
      user_id = extract_response.get("user_id")
      request.data["user"] = user_id


      # === METHOD :: GET ====
      if request.method == "GET":
            bookmark = get_object_or_404(Bookmark, pk=pk, user_id=user_id)
            serializer = BookmarkSerializer(bookmark)
            return Response(serializer.data, status=status.HTTP_200_OK)
      
      # === METHOD :: DELETE ===
      elif request.method == "DELETE":
            bookmark = get_object_or_404(Bookmark,pk=pk, user_id=user_id)

            if bookmark.is_trash:
                bookmark.delete()
                return Response({"message": "Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)
            else:
                bookmark.is_trash = True
                bookmark.save()
                return Response({"message": "Moved to Trash Successfully"}, status=status.HTTP_200_OK)

      tags = request.data.pop('tags', [])
      tag_instances = []
      for tag_name in tags:
            tag_serializer = TagSerializer(data={'name': tag_name})
            if tag_serializer.is_valid():
                  tag_instance, _ = Tag.objects.get_or_create(name=tag_name, user_id=user_id)
                  tag_instances.append(tag_instance)
            else:
                  return Response(tag_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      request.data['tags'] = [tag.id for tag in tag_instances]  # Convert tags to a list of tag IDs

      collection_name = request.data.get('collection')  # Assuming the collection name is passed in the request
      userInstance = User.objects.get(id=user_id)
      if collection_name :
            collection, _ = Collection.objects.get_or_create(name=collection_name, user=userInstance)
      else:
            collection, _ = Collection.objects.get_or_create(name="No Collection", user=userInstance)
      request.data["collection"]=collection.id

      # === METHOD :: PATCH ===
      if request.method == "PATCH":
            bookmark = get_object_or_404(Bookmark,pk=pk, user_id=user_id)

            
            # Try to update the thumbnail if "url" exists
            try:
                 url = extract_thumbnail(request.data["url"])
                 request.data["thumbnail_url"] = url
            except:
                 pass
            
            # Restore the bookmark from trash
            if "is_trash" in request.data and not request.data["is_trash"]:
                 if bookmark.is_trash:
                      bookmark.is_trash = False
                      bookmark.save()
                      return Response({"message": "Bookmark has been restored from a trash."}, status=status.HTTP_200_OK)

            serializer = BookmarkSerializer(instance=bookmark, data=request.data, partial=True)
            if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
      # === METHOD :: PUT ===
      elif request.method == "PUT":
            bookmark = get_object_or_404(Bookmark,pk=pk, user_id=user_id)

            # Update the thumbnail url for given "url" exists
            try:
                 url = extract_thumbnail(request.data["url"])
                 request.data["thumbnail_url"] = url
            except:
                 pass

            serializer = BookmarkSerializer(instance=bookmark, data=request.data)
            if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ======================================================
# === Get list of Collections ||  METHODS :: GET, POST
# ======================================================

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def collections_list(request):

    # ==== Extract the USER ID from token
    extract_response = extract_user_id_from_jwt(request)
    if "user_id" not in extract_response:
        return Response({ "error" : extract_response.get("error")})
    user_id = extract_response.get("user_id")
    request.data["user"] = user_id


    # ==== Method : GET ====
    if request.method == 'GET':
        collections = Collection.objects.filter(user_id=user_id)
        serializer = CollectionSerializer(collections, many=True)
        return Response(serializer.data)
    
    # ==== Method : POST ====
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ===========================================================
# === Operations on each Collection ||  METHODS :: GET, POST
# ===========================================================

@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def collections_detail(request, pk):
    
    # ==== Extract the USER ID from token ====
    extract_response = extract_user_id_from_jwt(request)
    if "user_id" not in extract_response:
        return Response({ "error" : extract_response.get("error")})
    user_id = extract_response.get("user_id")
    request.data["user"] = user_id

    
    # ==== Get the respected COLLECTION ====
    collection = get_object_or_404(Collection, pk=pk, user_id=user_id)


    # ==== Method : GET/PUT/PATCH/DELETE ====

    if request.method == "GET":
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = CollectionSerializer(instance=collection, data=request.data)
    elif request.method == "PATCH":
        serializer = CollectionSerializer(instance=collection, data=request.data, partial=True)
    elif request.method == "DELETE":
        collection.delete()
        return Response("Deleted Successfully", status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


    # ==== Save If Serializer object is valid ====
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ======================================================
# === Get list of Tags ||  METHODS :: GET, POST
# ======================================================

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def tags_list(request):
    
    # ==== Extract the USER ID from token ====
    extract_response = extract_user_id_from_jwt(request)
    if "user_id" not in extract_response:
        return Response({ "error" : extract_response.get("error")})
    user_id = extract_response.get("user_id")
    request.data["user"] = user_id


    # ==== GET and POST requests ====
    if request.method == 'GET':
        tags = Tag.objects.filter(user_id=user_id)
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# ==================================================================
# === Operations on each Tag ||  METHODS :: GET, PUT, PATCH, DELETE
# ==================================================================

@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def tags_detail(request, pk):

    # ==== Extract the USER ID from token ====
    extract_response = extract_user_id_from_jwt(request)
    if "user_id" not in extract_response:
        return Response({ "error" : extract_response.get("error")})
    user_id = extract_response.get("user_id")
    request.data["user"] = user_id


    # ==== Get the TAG object ====
    tag = get_object_or_404(Tag, pk=pk, user_id=user_id)


    # ==== Methods : GET | PUT | PATCH | DELETE ====
    if request.method == "GET":
        serializer = TagSerializer(tag)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = TagSerializer(instance=tag, data=request.data)
    elif request.method == "PATCH":
        serializer = TagSerializer(instance=tag, data=request.data, partial=True)
    elif request.method == "DELETE":
        tag.delete()
        return Response("Deleted Successfully", status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # ==== Save If Serializer object is valid ====
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def index(request):
      return JsonResponse({"msg" : "Hello"})

def extract_user_id_from_jwt(request):
    
    # ==== Get the token from REQUEST ====
    token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]

    try:
        # ==== Decode the token using the secret key used while creating token ====
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        
        # ==== Extract the user ID from JWT token ====
        user_id = decoded_token['user_id']
        
        # ==== Fetch the user object based on the user ID ====
        user = User.objects.get(id=user_id)
        
        return {'user_id': user_id, 'username': user.username}
    
    except jwt.ExpiredSignatureError:
        print("wwwwwwww")
        return redirect("http://localhost:8000/accounts/login")
        # return {'error': 'Token has expired', 'status':401}
    
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token', "status":401}
    
    except User.DoesNotExist:
        return {'error': 'User not found', "status":404}


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_bookmarks(request):
    
    # ==== Extract the USER ID from token ====
    extract_response = extract_user_id_from_jwt(request)
    if "user_id" not in extract_response:
        return Response({ "error" : extract_response.get("error")})
    user_id = extract_response.get("user_id")
    request.data["user"] = user_id


    search_query = request.query_params.get('query')
    if not search_query:
        return Response({"error": "Please provide a search query"}, status=status.HTTP_400_BAD_REQUEST)

    search_results = Bookmark.objects.filter(
        Q(title__icontains=search_query) | Q(url__icontains=search_query),
        user_id=user_id
    )

    serializer = BookmarkSerializer(search_results, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_csv(request, type, identifier=None):
    user_id = extract_user_id_from_jwt(request).get("user_id")

    if type == 'collection':
        try:
            collection = Collection.objects.get(name=identifier, user_id=user_id)
        except Collection.DoesNotExist:
            return Response({"error": "Collection not found"}, status=status.HTTP_404_NOT_FOUND)
        bookmarks = Bookmark.objects.filter(collection=collection, user_id=user_id)
        filename = f'{collection.name}_bookmarks.csv'

    elif type == 'tag':
        try:
            tag = Tag.objects.get(name=identifier, user_id=user_id)
        except Tag.DoesNotExist:
            return Response({"error": "Tag not found"}, status=status.HTTP_404_NOT_FOUND)
        bookmarks = Bookmark.objects.filter(tags=tag, user_id=user_id)
        filename = f'{tag.name}_bookmarks.csv'

    else:
        bookmarks = Bookmark.objects.filter(user_id=user_id)
        filename = 'all_bookmarks.csv'

    # Create the CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(['Title', 'URL', 'Description', 'Tags', 'Collection', 'Created At'])

    for bookmark in bookmarks:
        tag_names = ", ".join([tag.name for tag in bookmark.tags.all()])
        collection_name = bookmark.collection.name if bookmark.collection else "No Collection"
        writer.writerow([bookmark.title, bookmark.url, bookmark.description, tag_names, collection_name, bookmark.created_at])
    
    print(filename)
    return response
