from django.http import Http404
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from polls.forms import AnswerFormSerializer
from polls.models import get_full_poll, get_poll_questions, Poll
from polls.serializers import PollSerializer, DeepQuestionSerializer, ListPollSerializer


class PollView(views.APIView):
    serializer_class = PollSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, poll_id: int):
        queryset = get_full_poll(poll_id)
        poll = queryset.first()
        if poll is None:
            raise Http404
        serializer = self.serializer_class(poll)
        return Response(serializer.data)

    def post(self, request, poll_id: int):
        queryset = list(get_poll_questions(poll_id))
        serializer = AnswerFormSerializer(self.request.data, queryset)
        if serializer.is_valid:
            print('validated')
            serializer.save(self.request.user)
            return Response(status=201)
        else:
            return Response(status=400)


class PollListView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Вывод доступных опросов"""
        polls = Poll.objects.exclude(users__user=self.request.user)
        serializer = ListPollSerializer(polls, many=True)
        return Response(serializer.data)


class QuestionsPollView(views.APIView):
    serializer_class = DeepQuestionSerializer

    def get(self, request, poll_id: int):
        queryset = list(get_poll_questions(poll_id))
        serializer = self.serializer_class(queryset, many=True)
        data = {item['id']: item for item in serializer.data}
        return Response(data)
