from django.conf.urls.static import static
from django.urls import path

from config import settings
from core.maintenance.views import *

app_name = 'maintenance'

urlpatterns = [
    path('add/', MaintenanceCreateView.as_view(), name='create_maintenance'),
    path('list/', MaintenanceListView.as_view(), name='list_maintenance'),
    path('update/<int:pk>/', MaintenanceUpdateView.as_view(), name='update_maintenance'),
    path('detail/<int:pk>/', MaintenanceDetailView.as_view(), name='detail_maintenance'),
    path('detail_equipment/<int:pk>/', MaintenanceDetailEquipmentView.as_view(), name='detail_maintenance_equipment'),
    path('physical_record/', PhysicalRecordDownloadView.as_view(), name='physical_record'),
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
