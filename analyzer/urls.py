from django.urls import path

from . import views


urlpatterns = [
    path('', views.analyzer_home, name='analyzer_home'),
    path('api/sarvam/chat/', views.api_sarvam_chat, name='api_sarvam_chat'),
    path('api/sarvam/translate/', views.api_sarvam_translate, name='api_sarvam_translate'),
]

