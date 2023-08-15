from rest_framework import serializers
from .models import Bookmark, Tag, Collection

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = "__all__"
    
    def create(self, validated_data):
      print(validated_data)
      tags_data = validated_data.pop('tags', []) 
      bookmark = Bookmark.objects.create(**validated_data)

      for tag_data in tags_data:
            bookmark.tags.add(tag_data)
      
      return bookmark



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
    
    def create(self, validated_data):
        return Tag.objects.create(**validated_data)

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = "__all__"
    
    def create(self, validated_data):
        return Collection.objects.create(**validated_data)
