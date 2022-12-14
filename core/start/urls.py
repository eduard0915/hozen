from django.conf.urls.static import static
from django.urls import path

from config import settings
from core.start.views import StartView, NotPermsView

app_name = 'start'

urlpatterns = [
    path('', StartView.as_view(), name='start'),
    path('notperms/', NotPermsView.as_view(), name='notperms'),
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
