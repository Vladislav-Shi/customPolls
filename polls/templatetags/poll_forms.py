from typing import TypedDict, Optional

from django import template

register = template.Library()


class PollForm(TypedDict):
    poll_name: str
    description: Optional[str]
    questions: list


@register.inclusion_tag("forms/poll_form.html", takes_context=True)
def draw_form(context: dict, form: PollForm):
    data = {
        'name': form['poll_name'],
        'description': form.get('description'),
        'questions': form['questions'],

    }
    return data


@register.inclusion_tag(filename="forms/poll_field.html", takes_context=True)
def draw_poll_question(context: dict, question: dict):
    data = {
        'question': question,
    }
    return data
