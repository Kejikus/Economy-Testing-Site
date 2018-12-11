from django.shortcuts import render, redirect
from . import models
from django.db.models import Model
import random
from account.models import TestData


def testing(request):
    if not request.session.get('registered', False):
        request.session['context'] = {
            'errors': ('Register please to enter the test and don\'t refresh the testing page.',)
        }
        return redirect("account:register", permanent=True)

    user_data_id = request.session.get('user_data_id', None)

    if not user_data_id:
        return redirect("account:register", permanent=True)

    user_data = TestData.objects.get(id=user_data_id)

    questions = [
        {
            'type': question_to_set.question.content_type,
            'text': question_to_set.question.content,
            'is_open': question_to_set.question.is_open_question,
            'answers': question_to_set.question.answer_set.all(),
            'index': question_to_set.index,
        }
        for question_to_set in user_data.question_set.questiontoset_set.all()
    ]

    context = {
        'questions': questions,
        'user_data': user_data,
    }

    return render(request, 'testing.html', context)


def results(request):
    return render(request, 'results.html')
