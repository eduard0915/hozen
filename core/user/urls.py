from django.conf.urls.static import static
from django.urls import path

from config import settings
from core.user.views import *

app_name = 'user'

urlpatterns = [
    path('add/', UserCreateView.as_view(), name='user_create'),
    path('list/', UserListView.as_view(), name='user_list'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('update-password/<int:pk>/', UserPasswordUpdateView.as_view(), name='user_password_update'),
    path('detail/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('profile/<int:pk>/', MyProfileDetailView.as_view(), name='user_profile'),
    path('profile/edit/<int:pk>/', ProfileUpdateView.as_view(), name='user_profile_update'),
    path('edit/password/', UserChangePasswordView.as_view(), name='change_password'),
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
