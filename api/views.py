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
            bookmarks = Bookmark.objects.all()
            print(bookmarks[0])
            serializer = BookmarkSerializer(bookmarks, many=True)
            print(serializer.data)
            return Response(serializer.data)
      elif request.method == 'POST':

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
            
            try:
                 url = extract_thumbnail(request.data["url"])
                 request.data["thumbnail_url"] = url
                 print(request.data["thumbnail_url"] + "---" + request.data["url"])
            except:
                 pass

            serializer = BookmarkSerializer(data=request.data)
            if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data, status=status.HTTP_201_CREATED)
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
      
      # === METHOD :: POST ===
      elif request.method == "DELETE":
            bookmark = get_object_or_404(Bookmark,pk=pk)
            bookmark.delete()
            return Response("Deleted Successfully", status=status.HTTP_204_NO_CONTENT)

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
            serializer = BookmarkSerializer(instance=bookmark, data=request.data, partial=True)
            if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
      # === METHOD :: PUT ===
      elif request.method == "PUT":
            bookmark = get_object_or_404(Bookmark,pk=pk)
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