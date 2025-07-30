from rest_framework import serializers
from domain.aliment import Aliment

class AlimentSerializer(serializers.Serializer):
    '''
    Class that serialize/deserialize Aliment object(s)
    '''
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=500, allow_blank=True)
    status = serializers.BooleanField()

    def create(self, validated_data):
        return Aliment(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        return instance