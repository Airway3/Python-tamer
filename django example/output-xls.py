import os
import shutil
from functools import partial
from tempfile import TemporaryDirectory
import abc
import xlwt
from django.utils.decorators import classproperty


class BaseArchiveBuilder(abc.ABC):
    ARCHIVE_NAME = 'adverts'
    ARCHIVE_FORMAT = 'zip'
    ARCHIVE_PHOTO_FOLDER_NAME = 'photos'

    XLS_DOCUMENT_NAME = 'adverts.xls'
    XLS_FIELDS = ()

    @abc.abstractmethod
    def collect_info_from_adverts(self):
        """ Тут собирается инфа из объявления
        """

    def __init__(self, queryset, create_on_init=True):
        self._temp_dir = TemporaryDirectory()
        self.archive_path = os.path.join(self._temp_dir.name, self.archive_full_name)

        self.work_dir = self._make_folder(self._temp_dir.name, 'work_dir')
        self.photos_dir = self._make_folder(self.work_dir, self.ARCHIVE_PHOTO_FOLDER_NAME)

        self.queryset = queryset
        self.photos_index = 1

        self.wb = xlwt.Workbook()
        self.ws = self.wb.add_sheet('Объявления')

        if create_on_init:
            self.full_build()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._temp_dir.cleanup()

    def _make_folder(self, parent_dir, name):
        dir_name = os.path.join(parent_dir, name)
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        return dir_name

    def _collect_photos(self, advert):
        photos = []
        for photo in advert.photos.filter(enabled=True):
            photo_path = photo.image.file.name
            if os.path.isfile(photo_path):
                photo_name = str(self.photos_index) + os.path.splitext(photo_path)[1]
                shutil.copyfile(photo_path, os.path.join(self.photos_dir, photo_name))
                photos.append(photo_name)
                self.photos_index += 1
        return photos

    @classproperty
    def archive_full_name(cls):
        return '{}.{}'.format(cls.ARCHIVE_NAME, cls.ARCHIVE_FORMAT)

    def process_xls_document(self, save=False):
        for index, value in enumerate(self.XLS_FIELDS):
            self.ws.write(0, index, value)

        self.collect_info_from_adverts()
        if save:
            self.wb.save(os.path.join(self.work_dir, self.XLS_DOCUMENT_NAME))

    def make_archive(self, force=False):
        if os.path.exists(self.archive_path):
            if not force:
                os.remove(self.archive_path)
            else:
                raise FileExistsError('{} already exists'.format(self.archive_path))

        shutil.make_archive(
            os.path.join(self._temp_dir.name, self.ARCHIVE_NAME),
            self.ARCHIVE_FORMAT,
            self.work_dir
        )

    def full_build(self):
        self.process_xls_document(save=True)
        self.make_archive(force=True)
        return self.archive_path


class CommonBuilder(BaseArchiveBuilder):
    XLS_FIELDS = (
        'ID',
        'Город',
        'Заголовок',
        'Описание',
        'Цена',
        'Фото',
    )

    def collect_info_from_adverts(self):
        for advert_index, advert in enumerate(self.queryset, start=1):
            photos = self._collect_photos(advert)

            row_write = partial(self.ws.write, advert_index)
            row_write(0, advert_index)
            row_write(1, advert.city.title if advert.city else None)
            row_write(2, advert.title)
            row_write(3, advert.description)
            row_write(4, advert.price)
            row_write(5, ','.join(photos))


class ApartmentsBulder(BaseArchiveBuilder):
    XLS_FIELDS = (
        'ID',
        'Город',
        'Район',
        'Цена',
        'Валюта',
        'Период аренды',
        'Комнат в квартире',
        'Общая площадь (кв.м)',
        'Материал дома',
        'Этаж',
        'Этажей в здании',
        'Улица',
        'Дом',
        'Фото',
        'Описание'
    )

    def collect_info_from_adverts(self):
        for advert_index, advert in enumerate(self.queryset, start=1):
            photos = self._collect_photos(advert)

            row_write = partial(self.ws.write, advert_index)
            row_write(0, advert_index)
            row_write(1, advert.city.title if advert.city else None)
            row_write(2, advert.district.title if advert.district else None)
            row_write(3, advert.price)
            row_write(4, 'руб.')
            row_write(5, 'сутки')
            row_write(6, advert.rooms_number)
            row_write(7, advert.area_total)
            row_write(8, 'Кирпичный')  # что писать тут?
            row_write(9, advert.floor)
            row_write(10, advert.floors_total)
            row_write(11, advert.street.title if advert.street else None)
            row_write(12, advert.house_number)
            row_write(13, ','.join(photos))
            row_write(14, advert.description)

            self.ws.col(0).width = 1000
            self.ws.col(13).width = 10000
            self.ws.col(14).width = 20000


class KitchensBulder(BaseArchiveBuilder):
    XLS_FIELDS = (
        'ID',
        'Город',
        'Район',
        'Заголовок',
        'Описание',
        'Цена',
        'Фото',
    )

    def collect_info_from_adverts(self):
        for advert_index, advert in enumerate(self.queryset, start=1):
            photos = self._collect_photos(advert)

            row_write = partial(self.ws.write, advert_index)
            row_write(0, advert_index)
            row_write(1, advert.city.title if advert.city else None)
            row_write(2, advert.district.title if advert.district else None)
            row_write(3, advert.title)
            row_write(4, advert.description)
            row_write(5, advert.price)
            row_write(6, ','.join(photos))


class DryCleaningCarsBuilder(BaseArchiveBuilder):
    XLS_FIELDS = (
        'ID',
        'Город',
        'Метро',
        'Заголовок',
        'Описание',
        'Цена',
        'Фото',
    )

    def collect_info_from_adverts(self):
        for advert_index, advert in enumerate(self.queryset, start=1):
            photos = self._collect_photos(advert)

            row_write = partial(self.ws.write, advert_index)
            row_write(0, advert_index)
            row_write(1, advert.city.title if advert.city else None)
            row_write(2, advert.metro.title if advert.metro else None)
            row_write(3, advert.title)
            row_write(4, advert.description)
            row_write(5, advert.price)
            row_write(6, ','.join(photos))


class CottageBuilder(BaseArchiveBuilder):
    XLS_FIELDS = (
        'ID',
        'Город',
        'Заголовок',
        'Описание',
        'Цена',
        'Площадь дома',
        'Площадь участка',
        'Материал стен',
        'Количество этажей',
        'Фото',
    )

    def collect_info_from_adverts(self):
        for advert_index, advert in enumerate(self.queryset, start=1):
            photos = self._collect_photos(advert)

            row_write = partial(self.ws.write, advert_index)
            row_write(0, advert_index)
            row_write(1, advert.city.title if advert.city else None)
            row_write(2, advert.title)
            row_write(3, advert.description)
            row_write(4, advert.price)
            row_write(5, advert.area_house)
            row_write(6, advert.area_homestead)
            row_write(7, advert.wall_material)
            row_write(8, advert.floors_house)
            row_write(9, ','.join(photos))