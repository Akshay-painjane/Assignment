from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Field, TemplateMapping, DataTemplate
from .serializers import FieldSerializer, DataTemplateSerializer, TemplateMappingSerializer
from django.http import Http404
from .transformer import Transformer

# ------------------------------
# Field Operations (Create, Update, Delete)
# ------------------------------

class FieldListCreate(APIView):
    def get(self, request):
        try:
            fields = Field.objects.all()
            serializer = FieldSerializer(fields, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            # Handle both single and bulk creation
            if isinstance(request.data, list):
                serializer = FieldSerializer(data=request.data, many=True)
            else:
                serializer = FieldSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FieldDetailUpdateDelete(APIView):
    def get_object(self, pk):
        try:
            return Field.objects.get(pk=pk)
        except Field.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        try:
            field = self.get_object(pk)
            serializer = FieldSerializer(field, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response({"error": "Field not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            field = self.get_object(pk)
            field.delete()
            return Response({"message": "Field deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response({"error": "Field not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FieldBulkDelete(APIView):
    def delete(self, request):
        try:
            field_ids = request.data.get('ids', [])
            if not field_ids:
                return Response({"error": "No field ids provided"}, status=status.HTTP_400_BAD_REQUEST)

            fields_to_delete = Field.objects.filter(id__in=field_ids)
            deleted_count, _ = fields_to_delete.delete()

            if deleted_count == 0:
                return Response({"error": "No fields were deleted, check the ids"}, status=status.HTTP_404_NOT_FOUND)

            return Response({"message": f"Deleted {deleted_count} fields"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ------------------------------
# DataTemplate Operations
# ------------------------------

class DataTemplateListCreate(APIView):
    def get(self, request):
        try:
            templates = DataTemplate.objects.all()
            serializer = DataTemplateSerializer(templates, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            mappings_data = request.data.pop('mappings')

            # Create the DataTemplate
            data_template = DataTemplate.objects.create(name=request.data['name'])

            # Create TemplateMapping objects and associate them with the DataTemplate
            for mapping in mappings_data:
                source_field = Field.objects.get(pk=mapping['source_field'])
                destination_field = Field.objects.get(pk=mapping['destination_field'])
                template_mapping = TemplateMapping.objects.create(
                    source_field=source_field,
                    destination_field=destination_field
                )
                data_template.mappings.add(template_mapping)

            serializer = DataTemplateSerializer(data_template)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Field.DoesNotExist:
            return Response({"error": "Source or destination field does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DataTemplateUpdate(APIView):
    def put(self, request, pk):
        try:
            # Retrieve the existing data template
            data_template = DataTemplate.objects.get(pk=pk)
            # Update the name of the template
            data_template.name = request.data.get('name', data_template.name)
            data_template.save()  # Save the changes to the template

            # Clear existing mappings before adding new ones
            data_template.mappings.clear()

            # Handle the new mappings
            mappings_data = request.data.get('mappings', [])
            for mapping in mappings_data:
                # Verify existence of source and destination fields
                source_field = Field.objects.get(pk=mapping['source_field'])
                destination_field = Field.objects.get(pk=mapping['destination_field'])

                # Create a new mapping
                template_mapping = TemplateMapping.objects.create(
                    source_field=source_field,
                    destination_field=destination_field
                )
                data_template.mappings.add(template_mapping)

            return Response({"message": "Data template updated successfully"}, status=status.HTTP_200_OK)

        except DataTemplate.DoesNotExist:
            return Response({"error": "Data template not found"}, status=status.HTTP_404_NOT_FOUND)
        except Field.DoesNotExist:
            return Response({"error": "Source or destination field does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DataTemplateDelete(APIView):
    def delete(self, request, pk):
        try:
            # Retrieve the data template using the provided ID
            template = DataTemplate.objects.get(pk=pk)
            template.delete()  # Delete the template
            return Response({"message": "Data template deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except DataTemplate.DoesNotExist:
            return Response({"error": "Data template not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ------------------------------
# Transformer
# ------------------------------




class TransformData(APIView):
    def post(self, request, pk):
        try:
            template = DataTemplate.objects.get(pk=pk)

            input_data = request.data.get('input_data', {})
            transformer = Transformer()

            output_data = transformer.transform(input_data, template)
            return Response(output_data, status=status.HTTP_200_OK)

        except DataTemplate.DoesNotExist:
            return Response({"error": "Template not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
