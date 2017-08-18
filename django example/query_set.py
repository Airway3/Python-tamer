class Post(models.Model):
    title = models.CharField(max_length=255)
    #ещеполя...
    category = models.ForeignKey(Category,null=True,on_delete=models.SET_NULL)
    status = models.OneToOneField(PostStatus)
    tags = models.ManyToManyField(Tag)


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
для производителньости использовать:
value (выборка отдельных колонок, а не объектов) очень производительная шляпа когда много объектов и нам нужно конкретное поле

вместо циклов с "для каждого поста олл тегс" (а то будет столько запросов сколько и постов):
загружают сразу все связанные объекты с базы

select_related для форина и уан ту уан
prefetch_related для мени ту мени
'''

'''
create - оздание нового
update - обновить несколько
delete - удалить несколько
'''