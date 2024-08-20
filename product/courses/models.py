from django.conf import settings
from django.db import models


def get_default_course():
    return Course.objects.first()


class Course(models.Model):
    """Модель продукта - курса."""
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    start_date = models.DateTimeField(
        verbose_name='Дата и время начала курса'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name='Цена',
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name='Доступен ли курс для покупки',
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока."""
    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    link = models.URLField(
        max_length=250,
        verbose_name='Ссылка',
    )

    course = models.ForeignKey(
        Course,
        related_name='lessons',
        on_delete=models.CASCADE,
        default=get_default_course,
        verbose_name='Курс',
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Group(models.Model):
    """Модель группы."""
    course = models.ForeignKey(
        Course,
        related_name='groups',
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Курс',
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='student_groups',
        verbose_name='Студенты',
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('-id',)

    def __str__(self):
        return f'Группа {self.id} курса {self.course.title}' if self.course else f'Группа {self.id}'
