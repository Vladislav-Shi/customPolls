from django.urls import path

from polls.views import PollView, QuestionsPollView, PollListView

urlpatterns = [
    path('api/poll/<int:poll_id>', PollView.as_view()),
    path('api/questions/<int:poll_id>', QuestionsPollView.as_view()),
    path('api/polls/', PollListView.as_view()),
]
