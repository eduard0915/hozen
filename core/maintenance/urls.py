from django.conf.urls.static import static
from django.urls import path

from config import settings
from core.maintenance.views import *

app_name = 'maintenance'

urlpatterns = [
    path('add/', MaintenanceCreateView.as_view(), name='create_maintenance'),
    path('list/', MaintenanceListView.as_view(), name='list_maintenance'),
    # path('manufacturer_manual/', ManufacturerManualDownloadView.as_view(), name='manual_equipment'),
    # path('manufacturer_docs/', ManufacturerDocsDownloadView.as_view(), name='docs_equipment'),
    # path('update/<int:pk>/', EquipmentUpdateView.as_view(), name='update_equipment'),
    # path('detail/<int:pk>/', EquipmentDetailView.as_view(), name='detail_equipment'),
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
