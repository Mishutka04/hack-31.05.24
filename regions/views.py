from rest_framework import generics
from .models import Region
from .serializers import RegionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Trip, Vehicle
from .serializers import TripSerializer
import pandas as pd
#from statsmodels.tsa.statespace.sarimax import SARIMAX
#import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os
from config import settings
from django.shortcuts import render, get_object_or_404


class RegionListView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class RegionDetailView(generics.RetrieveAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

class TripMileageForecast(APIView):
    def get(self, request, vehicle_id, format=None):
        vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
        trips = Trip.objects.filter(vehicle_id=vehicle_id).order_by('trip_date')
        serializer = TripSerializer(trips, many=True)
        
        if len(trips)==0:
            return Response(trips, status=status.HTTP_404_NOT_FOUND)
        
        # Преобразование данных в DataFrame
        df = pd.DataFrame(serializer.data)
        df['trip_date'] = pd.to_datetime(df['trip_date'])
        df.set_index('trip_date', inplace=True)

        # Проверка наличия данных для прогнозирования
        if len(df) < 2:
            return Response({"error": "Not enough data for forecasting"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Параметры модели ARIMA
        order = (1, 1, 1)
        df['trip_mileage'] = pd.to_numeric(df["trip_mileage"])
        print(df['trip_mileage'])
        try:
            # Создание и обучение модели
            model = SARIMAX(df['trip_mileage'], order=order)
            model_fit = model.fit(disp=False)
            
            # Прогнозирование на следующие 5 периодов
            forecast_steps = 5
            forecast = model_fit.get_forecast(steps=forecast_steps)
            
            # Формирование индекса для прогнозируемых значений
            forecast_index = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=forecast_steps, freq='D')
            forecast_series = pd.Series(forecast.predicted_mean.values, index=forecast_index)
            
            # Построение графика прогнозируемых значений
            plt.figure(figsize=(12, 6))
            plt.plot(df['trip_mileage'], label='Наблюдаемые значения')
            plt.plot(forecast_series, label='Прогноз', linestyle='--', color='red')
            plt.xlabel('Дата', fontsize=12)
            plt.ylabel('Пробег, км', fontsize=12)
            plt.title('Прогноз пробега транспортных средств', fontsize=14)
            plt.legend(fontsize=12)
            plt.grid(True)
            
            # # Сохранение графика в буфер
            # buffer = BytesIO()
            # plt.savefig(buffer, format='png')
            # buffer.seek(0)
            # image_png = buffer.getvalue()
            # buffer.close()
            # image_base64 = base64.b64encode(image_png).decode('utf-8')
            # Сохранение графика
            image_path = os.path.join(settings.MEDIA_ROOT, f'forecast_plot_{vehicle_id}.png')
            plt.savefig(image_path, format='png')
            plt.close()

            # Формирование URL для изображения
            image_url = os.path.join(settings.MEDIA_URL, f'forecast_plot_{vehicle_id}.png')

            # Подготовка данных для ответа
            response_data = {
                # "observed_values": df['trip_mileage'].to_dict(),
                # "forecast_values": forecast_series.to_dict(),
                # "forecast_plot": image_base64
                "forecast_plot_url": request.build_absolute_uri(image_url)
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except IndexError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
