from typing import List

from rest_framework import serializers

from .models import Poll, Section, Question, Choice, QuestionCondition


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'


class QuestionConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionCondition
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    conditions = QuestionConditionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'


class DeepQuestionSerializer(QuestionSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        depth = 2


class SectionSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = '__all__'


class PollSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = '__all__'
        depth = 3


class ListPollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = '__all__'
        depth = 2
