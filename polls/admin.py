from django.contrib import admin
from django.db.models import TextField
from django.forms.widgets import Textarea
from nested_admin.forms import SortableHiddenMixin
from nested_admin.nested import NestedStackedInline, NestedModelAdmin, NestedTabularInline

from .models import Poll, Choice, Section, Question, QuestionCondition, UserPoll, Answer


class ChoiceInline(SortableHiddenMixin, NestedTabularInline):
    formfield_overrides = {
        TextField: {'widget': Textarea(attrs={
            'rows': "2", "cols": "55"})}
    }
    model = Choice
    extra = 0
    classes = ["collapse"]


class ConditionQuestionsInline(SortableHiddenMixin, NestedTabularInline):
    model = QuestionCondition
    extra = 0
    classes = ["collapse"]
    fk_name = 'question'


class QuestionInline(SortableHiddenMixin, NestedTabularInline):
    formfield_overrides = {
        TextField: {'widget': Textarea(attrs={
            'rows': "2", "cols": "55"})}
    }
    model = Question
    extra = 0
    inlines = [ChoiceInline, ConditionQuestionsInline]
    classes = ["collapse"]


class SectionInline(SortableHiddenMixin, NestedStackedInline):
    formfield_overrides = {
        TextField: {'widget': Textarea(attrs={
            'rows': "2", "cols": "55"})}
    }
    model = Section
    extra = 0
    inlines = [QuestionInline]


@admin.register(Poll)
class PollAdmin(NestedModelAdmin):
    formfield_overrides = {
        TextField: {'widget': Textarea(attrs={
            'rows': "2", "cols": "55"})}
    }
    fieldsets = [
        (
            None,
            {
                "fields": ["name", "description", "on_try"],
            }
        ),
    ]
    inlines = [SectionInline]


class AnswerInline(SortableHiddenMixin, NestedStackedInline):
    formfield_overrides = {
        TextField: {'widget': Textarea(attrs={
            'rows': "2", "cols": "55"})}
    }
    model = Answer
    extra = 0
    classes = ["collapse"]


@admin.register(UserPoll)
class UserPollAdmin(NestedModelAdmin):
    inlines = [AnswerInline]
    list_display = ['__str__', 'get_user', 'get_poll', 'update_at']

    def get_poll(self, obj):
        return obj.poll.name

    def get_user(self, obj):
        return obj.user.username


admin.site.register(Choice)
admin.site.register(Section)
admin.site.register(Question)
admin.site.register(Answer)
