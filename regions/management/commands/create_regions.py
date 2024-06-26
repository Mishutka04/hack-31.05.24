from django.core.management.base import BaseCommand
from regions.models import Region

REGIONS = [
    ('AD', 'Республика Адыгея'),
    ('AL', 'Республика Алтай'),
    ('BA', 'Республика Башкортостан'),
    ('BU', 'Республика Бурятия'),
    ('DA', 'Республика Дагестан'),
    ('IN', 'Республика Ингушетия'),
    ('KB', 'Кабардино-Балкарская Республика'),
    ('KL', 'Республика Калмыкия'),
    ('KC', 'Карачаево-Черкесская Республика'),
    ('KR', 'Республика Карелия'),
    ('KO', 'Республика Коми'),
    ('ME', 'Республика Марий Эл'),
    ('MO', 'Республика Мордовия'),
    ('SA', 'Республика Саха (Якутия)'),
    ('SE', 'Республика Северная Осетия - Алания'),
    ('TA', 'Республика Татарстан'),
    ('TY', 'Республика Тыва'),
    ('UD', 'Удмуртская Республика'),
    ('KK', 'Республика Хакасия'),
    ('CE', 'Чеченская Республика'),
    ('CU', 'Чувашская Республика'),
    ('ALT', 'Алтайский край'),
    ('KAM', 'Камчатский край'),
    ('KHA', 'Хабаровский край'),
    ('PRI', 'Приморский край'),
    ('STA', 'Ставропольский край'),
    ('KDA', 'Краснодарский край'),
    ('KYA', 'Красноярский край'),
    ('PER', 'Пермский край'),
    ('AMU', 'Амурская область'),
    ('ARK', 'Архангельская область'),
    ('AST', 'Астраханская область'),
    ('BEL', 'Белгородская область'),
    ('BRY', 'Брянская область'),
    ('CHE', 'Челябинская область'),
    ('IRK', 'Иркутская область'),
    ('IVA', 'Ивановская область'),
    ('KGD', 'Калининградская область'),
    ('KLU', 'Калужская область'),
    ('KEM', 'Кемеровская область'),
    ('KIR', 'Кировская область'),
    ('KOS', 'Костромская область'),
    ('KGN', 'Курганская область'),
    ('KRS', 'Курская область'),
    ('LEN', 'Ленинградская область'),
    ('LIP', 'Липецкая область'),
    ('MAG', 'Магаданская область'),
    ('MOS', 'Московская область'),
    ('MUR', 'Мурманская область'),
    ('NIZ', 'Нижегородская область'),
    ('NGR', 'Новгородская область'),
    ('NVS', 'Новосибирская область'),
    ('OMS', 'Омская область'),
    ('ORE', 'Оренбургская область'),
    ('ORL', 'Орловская область'),
    ('PNZ', 'Пензенская область'),
    ('PSK', 'Псковская область'),
    ('ROS', 'Ростовская область'),
    ('RYA', 'Рязанская область'),
    ('SAK', 'Сахалинская область'),
    ('SAM', 'Самарская область'),
    ('SAR', 'Саратовская область'),
    ('SMO', 'Смоленская область'),
    ('SVE', 'Свердловская область'),
    ('TAM', 'Тамбовская область'),
    ('TOM', 'Томская область'),
    ('TUL', 'Тульская область'),
    ('TVE', 'Тверская область'),
    ('TYU', 'Тюменская область'),
    ('ULY', 'Ульяновская область'),
    ('VLA', 'Владимирская область'),
    ('VGG', 'Волгоградская область'),
    ('VLG', 'Вологодская область'),
    ('VOR', 'Воронежская область'),
    ('YAR', 'Ярославская область'),
    ('MOW', 'Москва'),
    ('SPE', 'Санкт-Петербург'),
    ('YEV', 'Еврейская автономная область'),
    ('CHU', 'Чукотский автономный округ'),
    ('KHM', 'Ханты-Мансийский автономный округ - Югра'),
    ('YAN', 'Ямало-Ненецкий автономный округ'),
    ('NEN', 'Ненецкий автономный округ'),
]

class Command(BaseCommand):
    help = 'Create regions of Russia'

    def handle(self, *args, **options):
        for code, name in REGIONS:
            Region.objects.get_or_create(code=code, defaults={'name': name})
        self.stdout.write(self.style.SUCCESS('Successfully created or updated regions'))
