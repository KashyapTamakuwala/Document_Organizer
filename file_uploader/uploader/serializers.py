from rest_framework import serializers
from .models import File

class FileListSerializer(serializers.Serializer) :
    user_id = serializers.IntegerField()
    name = serializers.CharField(max_length=50)
    one_file = serializers.ListField(
                       child=serializers.FileField( max_length=100000,
                                         allow_empty_file=False,
                                         use_url=False )
                                )
    
    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        name=validated_data.pop('name')
        one_file=validated_data.pop('one_file')
        for file in one_file:
            f = File.objects.create(user_id=user_id,name=name, one_file=file,**validated_data)
        return f

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File  
        fields = '__all__'