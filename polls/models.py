import functools
import time
import uuid
from typing import List

from django.contrib.auth.models import User
from django.db import models, reset_queries, connection
from django.db.models import QuerySet


# Create your models here.
def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()

        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {end_queries - start_queries}")
        print(f"Finished in : {(end - start):.2f}s")
        return result

    return inner_func


class Poll(models.Model):
    """
    Модель опросника для динамического создания опросов
    """
    REWRITE = 'rewrite'
    ADD = 'add'
    ONE = 'one'

    QUESTION_TYPES = [
        (REWRITE, 'Переписать результат'),
        (ADD, 'Добавить новый'),
        (ONE, 'Запретить'),

    ]

    on_try = models.CharField(verbose_name='При повторном прохождении?', default=REWRITE, choices=QUESTION_TYPES,
                              max_length=32)
    name = models.CharField(verbose_name='Название опроса', max_length=255)
    description = models.TextField(verbose_name='Описание опроса', blank=True, null=True)
    uuid = models.UUIDField(verbose_name='UUID', default=uuid.uuid4, editable=False)

    def __str__(self) -> str:
        return f"{self.pk} - {self.name}"


class Section(models.Model):
    """
    Модель разделов опросов.
    Раздел -- набор вопросов. Тут же можно добавить условие появления опроса
    """
    name = models.CharField(verbose_name='Название секции', max_length=255)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, null=True, blank=True, related_name='sections')
    position = models.PositiveSmallIntegerField("Position", null=True)

    class Meta:
        verbose_name = 'Секция опроса'
        ordering = ['position']


class Question(models.Model):
    TEXT = 'text'
    SINGLE_CHOICE = 'single_choice'
    MULTIPLE_CHOICE = 'multiple_choice'

    QUESTION_TYPES = [
        (TEXT, 'Text'),
        (SINGLE_CHOICE, 'Single Choice'),
        (MULTIPLE_CHOICE, 'Multiple Choice'),

    ]

    survey = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    text = models.TextField(verbose_name='Текст вопроса')
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    other_field = models.BooleanField(verbose_name='Добавить поле "Другое"?', default=False)
    position = models.PositiveSmallIntegerField("Position", null=True)
    required = models.BooleanField(verbose_name='Обязательный вопрос?', default=False)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['position']

    def __str__(self):
        return f'{self.pk} - {self.text}  ({self.survey.poll.name})'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255, verbose_name='Текст варианта ответа')
    position = models.PositiveSmallIntegerField("Position", null=True)

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'
        ordering = ['position']



class QuestionCondition(models.Model):
    MORE_OR_EQ = '>='
    LESS_OR_EQ = '<='
    EQUAL = '=='
    NOT_EQUAL = '!='

    CONDITION_TYPES = [
        (EQUAL, '=='),
        (NOT_EQUAL, '!='),

    ]
    question_to_condition = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='conditions_operand')
    operation = models.CharField(max_length=20, choices=CONDITION_TYPES)
    question = models.ForeignKey(Question, related_name='conditions', on_delete=models.CASCADE)
    value = models.CharField(
        max_length=255)  # Условие, по которому определяется, должен ли быть показан следующий вопрос

    position = models.PositiveSmallIntegerField("Position", null=True)

    class Meta:
        verbose_name = 'Условие'
        verbose_name_plural = 'Условия'
        ordering = ['position']


class UserPoll(models.Model):
    """Опросы которые прошел пользвоатель (подразумевается,
     что в некоторых ситуациях 1 опрос может пройти несколько раз"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='users')
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.poll}'

    class Meta:
        verbose_name = 'Ответы Пользователя'
        verbose_name_plural = 'Ответы Пользователей'


class Answer(models.Model):
    poll_user = models.ForeignKey(UserPoll, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    answer = models.TextField(null=True, blank=True)
    old_text = models.CharField(max_length=255, null=True, blank=True)
    position = models.PositiveSmallIntegerField("Position", null=True)
    update_at = models.DateTimeField(auto_now=True)


def get_poll_questions(poll_id: int) -> QuerySet[Question]:
    """
    Получить все вопросы определенного опросника
    :param poll_name:
    :return List[Question]: Список вопросов оперделенного опросника. Нужно чтобы не плодилось много запросов в бд (тут всего 3)
    """
    poll = Question.objects.filter(survey__poll__pk=poll_id).select_related("survey__poll").prefetch_related(
        'choices').order_by('position')
    return poll


def get_full_poll(poll_id: int) -> Poll:
    """
    Получить полную структуру опроса
    :param poll_id:
    :return Poll: Опросник Тут уже много запросов в бд (5)
    """
    poll = Poll.objects.filter(pk=poll_id).prefetch_related('sections', 'sections__questions',
                                                                'sections__questions__choices',
                                                                'sections__questions__conditions')
    return poll
