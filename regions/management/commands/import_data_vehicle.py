import pandas as pd
from datetime import datetime
from django.core.management.base import BaseCommand
from regions.models import Region, Subdivision, Vehicle#, Trip, Telematics
from django.core.exceptions import ValidationError

regions_dict = {
    'ОКТЯБРЬСКАЯ ЖД': 'LEN',
    'КАЛИНИНГРАДСКАЯ ЖД': 'KGD',
    'ГОРЬКОВСКАЯ ЖД': 'NIZ',
    'МОСКОВСКАЯ ЖД': 'MOS',
    'СЕВЕРНАЯ ЖД': 'YAR'
}

class Command(BaseCommand):
    help = 'Импорт данных из XLSX файла'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Путь к XLSX файлу')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        self.import_data_from_xlsx(file_path)

    def import_data_from_xlsx(self, file_path):
        data = pd.read_excel(file_path)
        region_list=[]
        for _, row in data.iterrows():
            # region_name = row['Наименование полигона']
            region_list.append(row['Наименование полигона'])
            subdivision_name = row['Наименование структурного подразделения']
            if str(subdivision_name) == 'nan' or str(subdivision_name) == 'NaT':
                continue
            try:
                region_name = regions_dict[row['Наименование полигона']]
                subdivision_name = row['Наименование структурного подразделения']
                vehicle_number = row['Номерной знак ТС']
                trip_mileage=row['Данные путевых листов, пробег']
                driving_style=row['манера вождения']
                fines = row['Штрафы']
                region, _ = Region.objects.get_or_create(code=region_name)
                subdivision, _ = Subdivision.objects.get_or_create(name=subdivision_name, region=region)
                vehicle, _ = Vehicle.objects.get_or_create(
                    number=vehicle_number,
                    subdivision=subdivision,
                    all_telematics_mileage=trip_mileage,
                    driving_style=driving_style,
                    all_fines=fines
                    )
            except ValidationError:
                pass
        print(set(region_list))
            # trip_date=pd.to_datetime(row['дата путевого листа'], errors='coerce'),
            # print(row['Номерной знак ТС'], trip_date)

            # driving_style=row['манера вождения']
            # if str(driving_style) == 'nan' or str(driving_style) == 'NaT':
            #     driving_style=0
            
            # fines = row['Штрафы']
            # if str(fines) == 'nan' or str(fines) == 'NaT':
            #     fines=0
            
            # trip_date=pd.to_datetime(row['дата путевого листа'], errors='coerce')
            # if str(trip_date) == 'NaT':
            #     trip_date=None
            
            # trip_mileage=row['Данные путевых листов, пробег']
            # if str(trip_mileage) == 'nan' or str(trip_mileage) == 'NaT':
            #     trip_mileage=0
            
            # trip = Trip.objects.create(
            #     polygon_name=row['Наименование полигона'],
            #     short_name=row['Краткое наименование'],
            #     polygon=row['Полигон'],
            #     vehicle=vehicle,
            #     trip_date=trip_date,
            #     trip_mileage=trip_mileage,
            #     fines=fines,
            #     driving_style=driving_style
            # )

            # telematics_dates = str(row['Дата сигнала телематики']).split(';')
            # telematics_mileages = str(row['Данные телематики, пробег']).split(';')

            # for date, mileage in zip(telematics_dates, telematics_mileages):
            #     if date and mileage:
            #         Telematics.objects.create(
            #             trip=trip,
            #             telematics_date=pd.to_datetime(date, errors='coerce'),
            #             telematics_mileage=mileage
            #         )

# Запуск команды:
# python manage.py import_data path_to_your_file.xlsx
