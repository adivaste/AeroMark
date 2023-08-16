from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.models import Bookmark, Tag, Collection
from api.serializers import BookmarkSerializer, TagSerializer, CollectionSerializer
from django.http import JsonResponse
from django.contrib.auth.models import User
import time
from utils.getThumbnailURL import extract_thumbnail


# ===================================================
# === Get list of boookmarks ||  METHODS :: GET, POST
# ===================================================

@api_view(['GET', 'POST'])
def bookmarks_list(request):
     if request.method == 'GET':
        tag = None
        collection = None
        sort_by = 'recent'
        trash = False

        data = None

        # Check for sort by
        sort_possible_options = ['site_az', 'site_za', 'title_az', 'title_za', 'recent', 'older']
        req_sort_by = request.query_params.get('sort_by')
        if req_sort_by in sort_possible_options:
            sort_by = req_sort_by

        # Check for collection, tag, trash from request
        req_collection = request.query_params.get('collection')
        req_tag = request.query_params.get('tag')
        req_trash = request.query_params.get('trash')

        # Check for trash
        if req_trash is not None and req_trash == "True":
             trash=True

        # Check for collection
        if req_collection and Collection.objects.filter(name=req_collection).exists():
            collection = req_collection

        # Check for tags
        elif not req_collection and req_tag and Tag.objects.filter(name=req_tag).exists():
            tag = req_tag

        # Deciding what data to send
        if not collection and not tag:
            data = Bookmark.objects.all().filter()
        elif tag:
            data = Bookmark.objects.filter(tags__name=str(tag))
        else:
            data = Bookmark.objects.filter(collection__name=str(collection))

        if (trash):
             data = Bookmark.objects.filter(is_trash=True)
        else:
             data = data.filter(is_trash=False)
        


        # Deciding sorting order
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

            # Until Authentication is done, hardcoded user
            request.data['user'] = 1


            # Handles the tags, create and get instances
            tags = request.data.pop('tags', [])
            tag_instances = []
            for tag_name in tags:
                  tag_serializer = TagSerializer(data={'name': tag_name})
                  if tag_serializer.is_valid():
                        tag_instance, _ = Tag.objects.get_or_create(name=tag_name)
                        tag_instances.append(tag_instance)
                  else:
                        return Response(tag_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            request.data['tags'] = [tag.id for tag in tag_instances]  # Convert tags to a list of tag IDs


            # Getting collection instances or create it
            collection_name = request.data.get('collection')  
            userInstance = User.objects.get(id=1)
            if collection_name :
                  collection, _ = Collection.objects.get_or_create(name=collection_name, user=userInstance)
            else:
                  collection, _ = Collection.objects.get_or_create(name="No Collection", user=userInstance)

            request.data["collection"]=collection.id



            # Creating thumbnail
            try:
                 url = extract_thumbnail(request.data["url"])
                 request.data["thumbnail_url"] = url
                 print(request.data["thumbnail_url"] + "---" + request.data["url"])
            except:
                 pass
            

            # Creating the objects of models
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
def bookmarks_detail(request, pk):
      
      # === METHOD :: GET ====
      if request.method == "GET":
            bookmark = get_object_or_404(Bookmark,pk=pk)
            serializer = BookmarkSerializer(bookmark)
            return Response(serializer.data, status=status.HTTP_200_OK)
      
      # === METHOD :: DELETE ===
      elif request.method == "DELETE":
            bookmark = get_object_or_404(Bookmark,pk=pk)

            if bookmark.is_trash:
                bookmark.delete()
                return Response({"message": "Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)
            else:
                bookmark.is_trash = True
                bookmark.save()
                return Response({"message": "Moved to Trash Successfully"}, status=status.HTTP_200_OK)

      request.data['user'] = 1

      tags = request.data.pop('tags', [])
      tag_instances = []
      for tag_name in tags:
            tag_serializer = TagSerializer(data={'name': tag_name})
            if tag_serializer.is_valid():
                  tag_instance, _ = Tag.objects.get_or_create(name=tag_name)
                  tag_instances.append(tag_instance)
            else:
                  return Response(tag_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      request.data['tags'] = [tag.id for tag in tag_instances]  # Convert tags to a list of tag IDs

      collection_name = request.data.get('collection')  # Assuming the collection name is passed in the request
      userInstance = User.objects.get(id=1)
      if collection_name :
            collection, _ = Collection.objects.get_or_create(name=collection_name, user=userInstance)
      else:
            collection, _ = Collection.objects.get_or_create(name="No Collection", user=userInstance)
      request.data["collection"]=collection.id

      # === METHOD :: PATCH ===
      if request.method == "PATCH":
            bookmark = get_object_or_404(Bookmark,pk=pk)

            
            # Try to update the thumbnail if "url" exists
            try:
                 url = extract_thumbnail(request.data["url"])
                 request.data["thumbnail_url"] = url
            except:
                 pass


            serializer = BookmarkSerializer(instance=bookmark, data=request.data, partial=True)
            if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
      # === METHOD :: PUT ===
      elif request.method == "PUT":
            bookmark = get_object_or_404(Bookmark,pk=pk)

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
def collections_list(request):
    
    request.data['user'] = 1

    if request.method == 'GET':
        collections = Collection.objects.all()
        serializer = CollectionSerializer(collections, many=True)
        return Response(serializer.data)
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
def collections_detail(request, pk):
    
    request.data['user'] = 2

    collection = get_object_or_404(Collection, pk=pk)

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

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ======================================================
# === Get list of Tags ||  METHODS :: GET, POST
# ======================================================

@api_view(['GET', 'POST'])
def tags_list(request):
    if request.method == 'GET':
        tags = Tag.objects.all()
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
def tags_detail(request, pk):
    tag = get_object_or_404(Tag, pk=pk)

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

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def index(request):
      return JsonResponse({"msg" : "Hello"})