'''
https://djbook.ru/rel1.9/ref/contrib/contenttypes.html


class ContentTypeManager
Методы:
    get_for_id(id):
        Получить экземпляр ContentType по идентификатору(ID)
    get_for_model(model, for_concrete_model=True):
        Принимает в качестве аргумента либо класс модели, либо экземпляр модели, и возвращает экземпляр ContentType,
        представляющего данную модель. for_concrete_model=False позволяет получить ContentType для прокси-модели.
    get_for_models(*models, for_concrete_models=True):
        Принимает в качестве аргумента произвольное число классов модели и возвращает словарь с отображением класса модели
        на экземпляр ContentType, представляющего данную модель. for_concrete_model=False позволяет
        получить ContentType для прокси-модели.

from django.contrib.auth.models import User
ContentType.objects.get_for_model(User) #<ContentType: user>


class ContentType
Когда выполнился мигрейт, создаётся экземпляр ContentType для вашей модели.
Методы:
    ContentType.get_object_for_this_type(**kwargs):
        выполняет метод гет() модели. принимает фильтры в качестве аргументов возвращ один экз модели

    ContentType.model_class():
        возвращ класс модели

user_type = ContentType.objects.get(app_label="auth", model="user") #<ContentType: user>
user_type.model_class() #<class 'django.contrib.auth.models.User'>
user_type.get_object_for_this_type(username='Guido') #<User: Guido>


Generic relations

Вы можете использовать ContentType чтобы связать экземпляр вашей модели с любыми произвольными классами моделей проекта,
и использовать указанные методы для доступа к этим моделям.

Вы можете создать в вашей модели внешний ключ на ContentType, что позволит связать вашу модель с любой другой моделью,
как это было описано выше на примере Permission. Но можно пойти еще дальше и использовать ContentType для реализации
абсолютно обобщенных (иногда говорят “полиморфных”) отношений между моделями.

Вот простой пример: реализуем систему тэгов(ярлычков), которая могла бы выглядеть так:
'''

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class TaggedItem(models.Model):
    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id') # позволяет создать связь с любой моделью
    # нельзя юзать фильтер\эксклюд, также это поле не отображается в формах созданных по модели

    def __str__(self):              # __unicode__ on Python 2
        return self.tag

'''
Существуют три правила по созданию и настройке GenericForeignKey:

    Создайте в вашей модели поле типа ForeignKey, указав в качестве внешней модели ContentType.
    Обычно такому полю дают имя “content_type”.

    Создайте в вашей модели поле, которое будет хранить значения первичных ключей экземпляров модели,
    с которой вы создаете связь. Для большинства моделей, это поле типа PositiveIntegerField.
    Обычно такому полю дают имя “object_id”.

    Создайте в вашей модели поле типа GenericForeignKey, и передайте ему в качестве аргументов,
    имена полей созданных ранее. Если эти поля названы “content_type” и “object_id”, вы можете не передавать
    их, – эти имена используются в GenericForeignKey по умолчанию.

'''

# использование
from django.contrib.auth.models import User
guido = User.objects.get(username='Guido')
t = TaggedItem(content_object=guido, tag='bdfl') # связали экземпляр Юзер (гвидо) с тегом bdfl
t.save()
t.content_object # <User: Guido>


# НО!
# GenericForeignKey:
# 1. Не отображается в ModelForm
# 2. По этому полю нельзя ничего найти в запросах. (get/filter/exclude не сработают)
# для второго нужен related_query_name (по дефолту обратной не будет связи)

# class GenericRelation
# reverse generic relations
# чтобы иметь обратный доступ к TggedItems через Bookmark
# пример когда объект с которым нужна обратная свзяь заранее известен
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

class Bookmark(models.Model):
    url = models.URLField()
    tags = GenericRelation(TaggedItem)

b = Bookmark(url='https://www.djangoproject.com/')
b.save()
t1 = TaggedItem(content_object=b, tag='django')
t1.save()
t2 = TaggedItem(content_object=b, tag='python')
t2.save()
b.tags.all()
# [<TaggedItem: django>, <TaggedItem: python>]

# Создав GenericRelation с related_query_name, можно использовать связь в запросах:
tags = GenericRelation(TaggedItem, related_query_name='bookmarks')
# Это позволяет фильтровать, сортировать и выполнять запросы по Bookmark из TaggedItem:
TaggedItem.objects.filter(bookmarks__url__contains='django')
# [<TaggedItem: django>, <TaggedItem: python>]


# БЕЗ ОБРАТНОЙ СВЯЗИ ПОЛУЧАЕМ ОБЪЕКТ через букмарский контент тайп
b = Bookmark.objects.get(url='https://www.djangoproject.com/')
bookmark_type = ContentType.objects.get_for_model(b)
TaggedItem.objects.filter(content_type__pk=bookmark_type.id, object_id=b.id)
# [<TaggedItem: django>, <TaggedItem: python>]