'''
Поля связей
'''

class Post:
    category = models.ForeignKey(Category,null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True, # если юзер удалится, то это значение в таблице будет НУЛЛ в базе
    )
# аргумент on_delete применим к полям типа ForeignKey, OneToOneField
# что делать с постами когда удаляется категория?

# RESTRICT → models.PROTECT препятствует удалению связанного объекта вызывая исключение
# CASCADE → models.CASCADE удаляет объекты, связанные через ForeignKey
# SET NULL → models.SET_NULL устанавливает ForeignKey в NULL; возможно только если null равен True.
# NO ACTION → models.DO_NOTHING база решит что делать
# models.SET_DEFAULT устанавливает ForeignKey в значение по умолчанию; значение по-умолчанию должно быть указано для ForeignKey.