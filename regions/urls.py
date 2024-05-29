from django.urls import path
from .views import RegionListView, RegionDetailView


urlpatterns = [
    path(
        'regions/',
        RegionListView.as_view(),
        name='region-list-create'),
    path('regions/<str:pk>/',
         RegionDetailView.as_view(),
         name='region-detail'),
]
