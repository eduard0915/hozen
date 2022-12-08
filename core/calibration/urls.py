from django.conf.urls.static import static
from django.urls import path

from config import settings
from core.calibration.views import *

app_name = 'calibration'

urlpatterns = [
    path('add/', CalibrationCreateView.as_view(), name='create_calibration'),
    path('list/', CalibrationListView.as_view(), name='list_calibration'),
    path('update/<int:pk>/', CalibrationUpdateView.as_view(), name='update_calibration'),
    path('certificate/', CalibrationCertificateDownloadView.as_view(), name='certificate_calibration'),
    path('detail/<int:pk>/', CalibrationDetailView.as_view(), name='detail_calibration'),
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
