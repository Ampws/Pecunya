from django.urls import path
from .views import TelegramBotView

urlpatterns = [
    path('', TelegramBotView.as_view(), name='telegram_view'),
]