from django.db import models


class Posts(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    url = models.URLField()

    # Поскольку уже записанные строки могут обновляться (при записи данных нет входных фильтров на их новизну),
    # пусть будет записываться и дата этого изменения (вместо постоянной даты создания строки)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'id={self.id}'  # будем распознавать строки по id
