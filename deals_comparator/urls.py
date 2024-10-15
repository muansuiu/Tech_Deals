from django.urls import path
from .views import ComponentSearchAPIView

urlpatterns = [
    path('api/search/', ComponentSearchAPIView.as_view(), name='product-search'),
]