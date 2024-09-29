from rest_framework import serializers
from .models import Field, TemplateMapping, DataTemplate

# Field Serializer
class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = '__all__'


# TemplateMapping Serializer
class TemplateMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateMapping
        fields = '__all__'


# DataTemplate Serializer
class DataTemplateSerializer(serializers.ModelSerializer):
    mappings = TemplateMappingSerializer(many=True)

    class Meta:
        model = DataTemplate
        fields = '__all__'
