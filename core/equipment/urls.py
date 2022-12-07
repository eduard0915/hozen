from django.conf.urls.static import static
from django.urls import path

from config import settings
from core.equipment.views import *

app_name = 'equipment'

urlpatterns = [
    path('add/', EquipmentCreateView.as_view(), name='create_equipment'),
    path('list/', EquipmentListView.as_view(), name='list_equipment'),
    path('manufacturer_manual/', ManufacturerManualDownloadView.as_view(), name='manual_equipment'),
    path('manufacturer_docs/', ManufacturerDocsDownloadView.as_view(), name='docs_equipment'),
    path('update/<int:pk>/', EquipmentUpdateView.as_view(), name='update_equipment'),
    path('detail/<int:pk>/', EquipmentDetailView.as_view(), name='detail_equipment'),
    path('inactive/<int:pk>/', EquipmentInactiveView.as_view(), name='inactive_equipment'),
    path('active/<int:pk>/', EquipmentActiveView.as_view(), name='active_equipment'),
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
