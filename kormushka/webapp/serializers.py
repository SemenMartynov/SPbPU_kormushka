from rest_framework import serializers
from webapp.models import Category

# Serializers определ€ют представление API.
class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('name', )