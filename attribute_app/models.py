from django.db import models

# Field model for the Attribute Library
class Field(models.Model):
    name = models.CharField(max_length=100)
    visible_name = models.CharField(max_length=100)
    data_type = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# TemplateMapping model to map source fields to destination fields
class TemplateMapping(models.Model):
    source_field = models.ForeignKey(Field, related_name='source_field', on_delete=models.CASCADE)
    destination_field = models.ForeignKey(Field, related_name='destination_field', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.source_field.name} -> {self.destination_field.name}"


# DataTemplate model for the Data Template Engine, holding multiple mappings
class DataTemplate(models.Model):
    name = models.CharField(max_length=100)
    mappings = models.ManyToManyField(TemplateMapping, related_name='template_mappings')

    def __str__(self):
        return self.name
