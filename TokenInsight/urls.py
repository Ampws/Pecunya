from django.urls import path, include, re_path

from TokenInsight import consumers, views

urlpatterns = [
    # path('registration/account-confirm-email/<str:key>/', views.CustomVerifyEmailView.as_view(), name='account_confirm_email'),
    # path('registration/register/', views.CustomRegisterView.as_view(), name='account_register'),
    # path('registration/', include('dj_rest_auth.registration.urls')),
    # path('password/reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    # path('password/reset/confirm/<str:uidb64>/<str:token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('', include('dj_rest_auth.urls')),
]

websocket_urlpatterns = [
    re_path(r'ws/test1', consumers.TokenInsightConsumer.as_asgi()),
]