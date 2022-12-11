from django.conf.urls.static import static
from django.urls import path

from config import settings
from core.user.views import *

app_name = 'user'

urlpatterns = [
    path('add/', UserCreateView.as_view(), name='user_create'),
    path('list/', UserListView.as_view(), name='user_list'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('update_password/<int:pk>/', UserPasswordUpdateView.as_view(), name='user_password_update'),
    path('detail/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='user_profile'),
    path('inactive/<int:pk>/', UserInactiveView.as_view(), name='user_inactive'),
    path('active/<int:pk>/', UserActiveView.as_view(), name='user_active'),
    path('profile/edit/<int:pk>/', ProfileUpdateView.as_view(), name='user_profile_update'),
    path('edit/password/', UserChangePasswordView.as_view(), name='change_password'),
    # Formación académica
    path('add_academic/<int:pk>/', AcademicTrainingCreateView.as_view(), name='academic_create'),
    path('update_academic/<int:pk>/', AcademicTrainingUpdateView.as_view(), name='academic_update'),
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
