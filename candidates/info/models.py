from django.db import models


class Tag(models.Model):
    """Модель тега"""
    name = models.CharField(max_length=30, verbose_name='тэг', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Тэг'
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Skill(models.Model):
    """Модель навыка"""
    name = models.CharField(max_length=20, verbose_name='навык', null=True, blank=True)
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Навыки'
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'


class Candidate(models.Model):
    """Модель кандидата"""
    name = models.CharField(max_length=20, verbose_name='Имя', null=True, blank=True)
    surname = models.CharField(max_length=20, verbose_name='Фамилия', null=True, blank=True)
    lastname = models.CharField(max_length=20, verbose_name='Отчество', null=True, blank=True)
    tag = models.ManyToManyField(Tag, verbose_name='Тэг', null=True, blank=True)
    skill = models.ManyToManyField(Skill, verbose_name='Навык', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Кандидат'
        verbose_name = 'Кандидат'
        verbose_name_plural = 'Кандидаты'
