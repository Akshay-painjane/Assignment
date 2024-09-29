from django.urls import path
from .views import FieldListCreate, FieldDetailUpdateDelete, FieldBulkDelete, DataTemplateListCreate, TransformData,DataTemplateDelete,DataTemplateUpdate

urlpatterns = [
    path('fields/', FieldListCreate.as_view(), name='field-list-create'),
    path('fields/<int:pk>/', FieldDetailUpdateDelete.as_view(), name='field-detail'),
    path('fields/delete/', FieldBulkDelete.as_view(), name='field-bulk-delete'),
    path('templates/', DataTemplateListCreate.as_view(), name='template-list-create'),
    path('templates/<int:pk>/update/', DataTemplateUpdate.as_view(), name='template-update'),
    path('templates/<int:pk>/delete/', DataTemplateDelete.as_view(), name='template-delete'),
    path('transform/<int:pk>/', TransformData.as_view(), name='transform-data'),
]
