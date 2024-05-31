from django.db import models

class Region(models.Model):
    REGION_CHOICES = [
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

    code = models.CharField(max_length=3, choices=REGION_CHOICES, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'
    
    @property
    def vehicles_count(self):
        vehicles = 0
        subdivisions = self.subdivisions.all()
        for sub in subdivisions:
            vehicles+=len(sub.vehicles.all())
        # for product in products:
        #     sum_try = sum_try + sum(
        #         [purchase.price_try for purchase in product.purchases.all()])
        return vehicles


class Subdivision(models.Model):
    name = models.CharField(
        max_length=255,
        # unique=True,
        verbose_name='Наименование структурного подразделения')
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE,
        related_name='subdivisions',
        verbose_name='Регион')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Структурное подразделение'
        verbose_name_plural = 'Структурные подразделения'
    
    @property
    def vehicles_count(self):
        vehicles = self.vehicles.all()
        return len(vehicles)

class Vehicle(models.Model):
    number = models.CharField(
        max_length=50,
        verbose_name='Номерной знак ТС')
    subdivision = models.ForeignKey(
        Subdivision,
        on_delete=models.CASCADE,
        related_name='vehicles',
        verbose_name='Структурное подразделение')
    driving_style = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0,
        verbose_name='Манера вождения')
    all_fines = models.IntegerField(
        default=0,
        verbose_name='Штрафы')
    all_telematics_mileage = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Данные телематики, пробег')
    in_structure = models.BooleanField(
        default=False,
        verbose_name='В структуре парка'
        )

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = 'Транспортное средство'
        verbose_name_plural = 'Транспортные средства'

class Trip(models.Model):
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='trips',
        verbose_name='Транспортное средство')
    trip_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата путевого листа')
    trip_mileage = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Данные путевых листов, пробег')
    telematics_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата сигнала телематики')
    telematics_mileage = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Данные телематики, пробег')

    def __str__(self):
        return f'{self.vehicle.number}'

    class Meta:
        verbose_name = 'Путевой лист'
        verbose_name_plural = 'Путевые листы'