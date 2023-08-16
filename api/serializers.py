from rest_framework import serializers
from .models import Bookmark, Tag, Collection
from django.contrib.auth.models import User


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('name',)

    # For the POST request, create the object of Model "Tag"
    def create(self, validated_data):
        return Tag.objects.create(**validated_data)


class BookmarkSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Bookmark
        fields = "__all__"


    # For the POST request, create the object of Model "Bookmark"
    def create(self, validated_data):
      tags_data = validated_data.pop('tags', []) 
      bookmark = Bookmark.objects.create(**validated_data)

      for tag_data in tags_data:
            bookmark.tags.add(tag_data)
      
      return bookmark


    # Convert tag, user, collection to string format instead of pk's
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = str(User.objects.get(id=data['user']))
        data['collection'] = str(Collection.objects.get(id=data['collection']))

        tempTags = []
        for tagId in data['tags'] :
            tagName = str(Tag.objects.get(pk=int(tagId)))
            tempTags.append(tagName)
        data['tags'] = tempTags

        return data


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = "__all__"
    
    # For the POST request, create the object of Model "Collection"
    def create(self, validated_data):
        return Collection.objects.create(**validated_data)
