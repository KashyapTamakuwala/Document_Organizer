from rest_framework import serializers
from .models import FolderDetails, Dataobject


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model=FolderDetails
        fields = '__all__'
