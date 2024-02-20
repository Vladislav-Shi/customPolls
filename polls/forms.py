import re
from typing import List

from django.contrib.auth.models import User
from django.http import HttpRequest

from polls.models import Question, Poll, UserPoll, Answer
from polls.serializers import DeepQuestionSerializer

class AnswerFormSerializer:
    # TODO переписать на Serializer
    questions: List[Question]

    def __init__(self, request_data: dict, questions: List[Question]):
        if len(questions) == 0:
            raise ValueError('В данной форме нет вопросов')
        if len(questions) == 0:
            raise ValueError('Пустой ответ')
        self.raw_form = request_data
        self.questions = questions
        serialize = DeepQuestionSerializer(questions, many=True)
        self.serialized_questions = {question['id']: question for question in serialize.data}
        self.prepared_form = None

        self.prepare_raw_form()
        self.is_valid = self.validate()
        self.add_choice_in_form()

    def prepare_raw_form(self):
        """Заменяет все field__n на n. при этом убирает с пустой формы "лишние" поля"""
        form_data = {}
        for key, value in self.raw_form.items():
            key = key.split('__')
            if key[0] != 'field' or len(key) != 2:
                continue
            form_data[int(key[1])] = value

        self.raw_form = form_data
        self.prepared_form = form_data

    def validate(self) -> bool:
        """Проверяет что все нужные поля заполнены и заполнены допустимыми значениями"""
        for question in self.serialized_questions.values():
            if question['id'] not in self.raw_form:
                self.raw_form[question['id']] = None
            form_question = self.raw_form[question['id']]
            if not question['required'] and form_question in [None, '']:
                continue
            if form_question in [None, ''] and question['required']:
                return False
            if question['question_type'] in ['single_choice', 'multiple_choice']:
                if question['question_type'] == 'single_choice':
                    form_choice = {form_question}
                else:
                    form_choice = set(form_question)
                choices = {f"${choice['id']}" for choice in question['choices']}
                if form_choice.issubset(choices):
                    continue
                if not question['other_field']:
                    return False
        return True

    def add_choice_in_form(self):
        """Заполняет все $n значениями соответсвующего выбора"""
        for q_id in self.raw_form.keys():
            question = self.serialized_questions[q_id]
            if len(question['choices']) > 0:
                form_question = self.raw_form[q_id]
                choice_values = {choice['id']: choice['text'] for choice in question['choices']}
                if isinstance(form_question, str) and form_question.startswith('$'):
                    match = re.search(r'\d+', form_question)
                    self.prepared_form[q_id] = choice_values[int(match.group())]
                elif isinstance(form_question, list):

                    for index, answer in enumerate(form_question):
                        if answer.startswith('$'):
                            match = re.search(r'\d+', answer)
                            self.prepared_form[q_id][index] = choice_values[int(match.group())]

    def save(self, user: User):
        write_option = self.questions[0].survey.poll.on_try
        poll_id = self.questions[0].survey.poll.id
        user_poll = UserPoll.objects.filter(user=user, poll_id=poll_id).last()

        if user_poll is not None and write_option == Poll.ONE:
            raise ValueError('На каждого пользователя только по одной записи')
        if user_poll is not None and write_option == Poll.REWRITE:
            user_poll.answers.all().delete()
        else:
            user_poll = UserPoll.objects.create(user_id=1, poll_id=poll_id)
        objects = [Answer(
            poll_user_id=user_poll.id,
            question_id=key,
            answer=str(value),
            old_text=self.serialized_questions[key]['text']
        ) for key, value in self.prepared_form.items()]
        Answer.objects.bulk_create(objects)
