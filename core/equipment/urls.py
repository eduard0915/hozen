from django.conf.urls.static import static
from django.urls import path

from config import settings
from core.equipment.views import *

app_name = 'equipment'

urlpatterns = [
    path('add/', EquipmentCreateView.as_view(), name='create_equipment'),
    path('list/', EquipmentListView.as_view(), name='list_equipment'),
    path('update/<int:pk>/', EquipmentUpdateView.as_view(), name='update_equipment'),
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
