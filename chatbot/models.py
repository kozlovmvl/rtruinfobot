from django.db import models


class Answer(models.Model):
    parent = models.ForeignKey(
        'Answer', on_delete=models.SET_NULL, 
        null=True, default=None, blank=True,
        verbose_name='предшественник')
    text = models.TextField(verbose_name='текст')
    TYPE_CHOICES = (('text', 'Текст'), ('button', 'Кнопка'))
    type = models.CharField(
        max_length=50, choices=TYPE_CHOICES, 
        default='text', verbose_name='тип')

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
    
    @classmethod
    def get_start(cls):
        start_message = cls.objects.values('id', 'text').get(parent_id=None)
        return dict(start_message)

    @classmethod
    def get_list(cls, parent_id):
        list_messages = cls.objects.filter(parent_id=parent_id)\
            .order_by('text').values('id', 'text', 'type')
        return list(list_messages)

    def __str__(self):
        return self.text[:50]
