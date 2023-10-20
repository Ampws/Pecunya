from django.urls import path, include

urlpatterns = [
    path('api/Auth/', include('Auth.urls')),
    path('api/TokenInsight/', include('TokenInsight.urls')),
    path('api/Telegram/', include('Telegram.urls')),
]