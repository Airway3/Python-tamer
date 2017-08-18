from collections import namedtuple

from libs.utils import ChoicesHelper

# модули
CHANGE_FORMS_MODULE = 'apps.adverts_v2.forms'
ARCHIVE_BUILDERS_MODULE = 'apps.adverts_v2.builders'
SCRAPY_DJANGO_ITEMS_MODULES = 'parsing.items'

# Фотографии
ADVERTS_PHOTOS_PATH = 'adverts/photos'
ADVERTS_PHOTOS_SMALL_SIZE = (200, 150)

# Доноры объявлений
DUMMY = 999
DUMMY_URL = 'http://dummy.donor/{}'

EST = 0
PRINTEREST = 1
TIU = 2
AVITO = 3
DONORS_FULL = (
    (EST, 'est.ua', {}),
    (PRINTEREST, 'printerest.com', {}),
    (TIU, 'tiu.ru', {}),
    (AVITO, 'avito.ru', {}),
    (DUMMY, 'DUMMY', {}),
)
DONORS = ChoicesHelper.make(DONORS_FULL)

# Состояние квартиры
DISINERS = 0
EURO = 1
COSMETIC = 2
CAPITAL = 3
AFTER_RECONSTRUCTION = 4
RESIDENTAL = 5
NEED_COSMETIC = 6
FOR_FINISHING = 7
NEED_CAPITAL = 8
UNFINISHED_CONSTRUCTION = 9
WITHOUT_REPAIR = 10

CONDITIONS_FULL = (
    (DISINERS, 'дизайнерский ремонт', {
        'aliases': [],
    }),
    (EURO, 'евроремонт', {
        'aliases': [],
    }),
    (COSMETIC, 'косметический ремонт', {
        'aliases': [],
    }),
    (CAPITAL, 'капитальный ремонт', {
        'aliases': [],
    }),
    (AFTER_RECONSTRUCTION, 'после реконструкции', {
        'aliases': [],
    }),
    (RESIDENTAL, 'жилое/советское', {
        'aliases': [],
    }),
    (NEED_COSMETIC, 'требуется косметический ремонт', {
        'aliases': [],
    }),
    (FOR_FINISHING, 'под чистовую отделку', {
        'aliases': [],
    }),
    (NEED_CAPITAL, 'требуется капитальный ремонт', {
        'aliases': [],
    }),
    (UNFINISHED_CONSTRUCTION, 'незавершённое строительство', {
        'aliases': [],
    }),
    (WITHOUT_REPAIR, 'без ремонта', {
        'aliases': [],
    }),
)
CONDITIONS_CHOICES = ChoicesHelper.make(CONDITIONS_FULL)

# Тип квартиры
SEPARATE = 0
COMMUNAL = 1
SMALL_FAMILY = 2
DUPLEX = 3
STUDIO = 4
HOSTEL = 5

APARTMENT_TYPES_FULL = (
    (SEPARATE, 'отдельная', {
        'aliases': [],
    }),
    (COMMUNAL, 'коммунальная', {
        'aliases': [],
    }),
    (SMALL_FAMILY, 'малосемейка', {
        'aliases': [],
    }),
    (DUPLEX, 'двухуровневая', {
        'aliases': [],
    }),
    (STUDIO, 'студия', {
        'aliases': [],
    }),
    (HOSTEL, 'общежитие', {
        'aliases': [],
    }),
)
APARTMENT_TYPES_CHOICES = ChoicesHelper.make(APARTMENT_TYPES_FULL)

# Статусы объявлений
NEW = 0
REJECTED = 1
USED = 2
IN_WORK = 3
ADVERT_STATUSES_FULL = (
    (NEW, 'Новое', {
        'url_name': 'adverts_v2:new-adverts',
        'name_plural': 'Новые',
        'button_name': 'В новые',
    }),
    (REJECTED, 'Отклоненное', {
        'url_name': 'adverts_v2:rejected-adverts',
        'name_plural': 'Отклоненные',
        'button_name': 'В отклоненные',
    }),
    (USED, 'Использованное', {
        'url_name': 'adverts_v2:used-adverts',
        'name_plural': 'Использованные',
        'button_name': 'В использованные',
    }),
    (IN_WORK, 'В работе', {
        'url_name': 'adverts_v2:adverts-in-work',
        'name_plural': 'В работе',
        'button_name': 'В работу',
    }),

)
ADVERT_STATUSES = ChoicesHelper.make(ADVERT_STATUSES_FULL)


BRICK = 0
BLOCK = 1
PANEL = 2
MONOLITH = 3

HOUSE_MATERIALS = (
    (BRICK, 'Кирпичный'),
    (BLOCK, 'Блочный'),
    (PANEL, 'Панельный'),
    (MONOLITH, 'Монолитный'),
)
HOUSE_MATERIALS_VALUES = tuple(value for value, title in HOUSE_MATERIALS)

# количество объявлений на странице
ADVERTS_ON_PAGE = 10

# Количество характеристик объявления в списке
ADVERT_DETALIZATION_ITEMS_LIMIT = 0

# Поля для которых генеруется тексе
AUTO_GENERATED_FIELDS = ('title', 'description')

#Базовый конфиг категорий
CategoryConfig = namedtuple('CategoryConfig', field_names=(
    'change_form_class',
    'archive_builder_class',
    'auto_generated_fields'
))

# Категории (Model._meta.model_name == category)
# TODO: пока так, потом можно перенести в бд, если будет много
UNDEFINED = 'UNDEFINED_CATEGORY'
APARTMENTS = 'apartmentadvert'
KITCHENS = 'kitchenadvert'
CHILDREN_WEAR = 'childrenwearadvert'
STRETCH_CEILING = 'stretchceilingadvert'
DRY_CLEANING_CARS = 'drycleaningcarsadvert'
CLEANING_SERVICE = 'cleaningserviceadvert'

CATEGORIES_CONFIG = (
    (APARTMENTS, 'Квартиры в аренду', CategoryConfig(
        change_form_class='ApartmentForm',
        archive_builder_class='ApartmentsBulder',
        auto_generated_fields=('description', ),
    )),
    (KITCHENS, 'Кухни', CategoryConfig(
        change_form_class='KitchenForm',
        archive_builder_class='KitchensBulder',
        auto_generated_fields=('title', 'description'),
    )),
    (CHILDREN_WEAR, 'Детская одежда', CategoryConfig(
        change_form_class='ChildrenWearForm',
        archive_builder_class='CommonBuilder',
        auto_generated_fields=('title', 'description'),
    )),
    (STRETCH_CEILING, 'Натяжные потолки', CategoryConfig(
        change_form_class='StretchCeilingForm',
        archive_builder_class='CommonBuilder',
        auto_generated_fields=('title', 'description'),
    )),
    (DRY_CLEANING_CARS, 'Химчистка авто', CategoryConfig(
        change_form_class='DryCleaningCarsForm',
        archive_builder_class='DryCleaningCarsBuilder',
        auto_generated_fields=('title', 'description'),
    )),
    (CLEANING_SERVICE, 'Клининг', CategoryConfig(
        change_form_class='CleaningServiceForm',
        archive_builder_class='CommonBuilder',
        auto_generated_fields=('title', 'description'),
    )),
)
CATEGORIES_CHOICES = ChoicesHelper.make(CATEGORIES_CONFIG)
CATEGORIES_PATTERN = '|'.join(name for name, _ in CATEGORIES_CHOICES)