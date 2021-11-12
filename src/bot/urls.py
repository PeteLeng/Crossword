from django.urls import path
from .views import (
    AssembleView,
    AssembleDetailView,
)

app_name = 'bot'
urlpatterns = [
    path('', AssembleView.as_view(), name='bot-assemble'),
    path('<int:id1>/', AssembleDetailView.as_view(), name='bot-assemble-detail'),
    # path('assemble/<int:id1>/', AssembleDetailViewCache.as_view(), name='bot-assemble-detail-cache'),
]