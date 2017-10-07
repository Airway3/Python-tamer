class Post(models.Model):
    title = models.CharField(max_length=255)
    #ещеполя...
    category = models.ForeignKey(Category,null=True,on_delete=models.SET_NULL)
    status = models.OneToOneField(PostStatus)
    tags = models.ManyToManyField(Tag)

Через менеджер модели (как минимум один по умолчанию здесь Post.objects, обратиться можно ток через модель)
мы получаем кверисеты.
Добавление дополнительных методов в Manager - лучший способ добавить “table-level” функционал в вашу модель.
(Для “row-level” функционала – то есть функции, которые работают с одним экземпляром модели – используйте методы модели,
 а не методы менеджера.)
У менеджера есть базовый кверисет, который он возвращает.
class DahlBookManager(models.Manager):
    def get_queryset(self):
        return super(DahlBookManager, self).get_queryset().filter(author='Roald Dahl')
    
Book.dahl_objects.all() Returns a new QuerySet that is a copy of the current one.
    
post = Post.objects.get(pk=1) # Post
category = post.category # Category можно обращаться к её атрибутам
category_id = post.category_id # int значение из базы. это поле создано было автоматически в экзмепляре модели пост
status = post.status # Status
status_id = post.status_id # int значение из базы. это поле создано было автоматически в экзмепляре модели пост
tags_manager = post.tags # RelatedManager
post.tags.all() #[Tags]

# #использование обратного отношения
category.post_set.all() # все связанные [Post] ForeignKey с поста на категорию при обращении от категории возвращает релейтед менеджер
tag = Tag.objects.get(pk=1)
tag.post_set.all() # все связанные [Post] мени ту мени всегда через релейтед менеджер



'''
Методы возвращающие кверисет (чейн):
all (копия кверисета к которому применён / Returns a new QuerySet that is a copy of the current one),
filter, exclude, annotate, order_by, reverse, distinct
Методы возвращающие кверисетоподобные объекты: 
1) values - Полезен, если вам нужны только данные некоторых полей и не нужен функционал объектов моделей.
    # This list contains a Blog object.
    >>> Blog.objects.filter(name__startswith='Beatles')
    [<Blog: Beatles Blog>]

    # This list contains a dictionary.
    >>> Blog.objects.filter(name__startswith='Beatles').values()
    [{'id': 1, 'name': 'Beatles Blog', 'tagline': 'All the latest Beatles news.'}]
2) values_list - вместо словаря возвращает кортеж
    >>> Entry.objects.values_list('id', 'headline')
    [(1, 'First entry'), ...]
    Если вы указали одно поле, можете указать аргумент flat.
    При True, каждая запись будет возвращена как отдельное значение, а не одноэлементный кортеж.
    Значение поля из определенной записи:
        >>> Entry.objects.values_list('headline', flat=True).get(pk=1)
        'First entry'



Что использовать в типичных случаях?
1) узнаём количество объектов методом count у queryset, а не len.
2) узнаём существуют ли объекты через метод exists:
    entry = Entry.objects.get(pk=123)
    if some_queryset.filter(pk=entry.pk).exists():
        print("Entry contained in queryset")
   если результат всё же нужен, то выгоднее проверять так  bool(some_queryset) и дальше использовать объекты
3) случайная сортировка Entry.objects.order_by('?') грузит базу
4) для производителньости использовать value (выборка отдельных колонок, а не объектов)
очень производительная шляпа когда много объектов и нам нужно конкретное поле

5) вместо циклов с "для каждого поста олл тегс" (а то будет столько запросов сколько и постов):
загружают сразу все связанные объекты с базы:
    a) select_related
Вы можете указать любое ForeignKey или OneToOneField поле в select_related().
Несколько вызовов select_related теперь работает как и для других методов – то есть select_related('foo', 'bar').
Возвращает QuerySet который автоматически включает в выборку данные связанных объектов при выполнении запроса:
    без
        # Hits the database.
        e = Entry.objects.get(id=5)

        # Hits the database again to get the related Blog object.
        b = e.blog №связанный форином объект

    с ним
        # Hits the database.
        e = Entry.objects.select_related('blog').get(id=5)

        # Doesn't hit the database, because e.blog has been prepopulated
        # in the previous query.
        b = e.blog
    
    b) prefetch_related
выбирает данные для каждой связи отдельно, и выполняет “объединение” на уровне Python
'''
