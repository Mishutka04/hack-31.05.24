from django.urls import path
from .views import RegionListView, RegionDetailView, TripMileageForecast


app_name="regions"
urlpatterns = [
    path(
        'regions/',
        RegionListView.as_view(),
        name='region-list-create'),
    path('regions/<str:pk>/',
         RegionDetailView.as_view(),
         name='region-detail'),
    path(
        'forecast_trip/<int:vehicle_id>/',
        TripMileageForecast.as_view(),
        name='trip-mileage-forecast'),
]
