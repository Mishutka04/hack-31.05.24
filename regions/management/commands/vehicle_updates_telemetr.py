import pandas as pd
from django.core.management.base import BaseCommand
from regions.models import Region, Subdivision, Vehicle, Trip
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
        for i in list(regions_dict.keys()):
            df = pd.read_excel(file_path, header=None)

            # Условие для определения строк, содержащих "МОСКОВСКАЯ ЖД"
            # target_text = "МОСКОВСКАЯ ЖД"
            target_text=i
            is_target_row = df.iloc[:, 0] == target_text
            indices = df[is_target_row].index

            # Словарь для хранения результатов
            results = {}

            for index in indices:
                key = tuple(df.iloc[index])  # Ключем будет кортеж со значениями строки "МОСКОВСКАЯ ЖД"
                values = []
                
                next_index = index + 1
                while next_index < len(df) and pd.isna(df.iloc[next_index, 0]):
                    values.append(tuple(df.iloc[next_index]))  # Добавляем строку в список значений
                    next_index += 1
                
                results[key] = values

            # Вывод результата
            for key, value in list(results.items()):
                print(f"Key: {key[9], key[11]}")
                subdivision_name = key[4]
                try:
                    subdivision = Subdivision.objects.get(name=subdivision_name)
                except Subdivision.DoesNotExist:
                    continue
                vehicle_number = key[3]
                all_fines = key[-2]
                driving_style = key[-1]
                if str(driving_style) == 'nan' or str(driving_style) == 'NaT':
                    driving_style=0
                all_true_telematics_mileage=key[11]
                if str(all_true_telematics_mileage) == 'nan' or str(all_true_telematics_mileage) == 'NaT':
                    all_true_telematics_mileage=0
                try:
                    vehicle = Vehicle.objects.filter(
                        number=vehicle_number,
                        subdivision=subdivision,
                        driving_style=driving_style,
                        all_fines=all_fines,
                        ).update(
                            all_true_telematics_mileage=all_true_telematics_mileage)
                except Vehicle.DoesNotExist:
                    continue
