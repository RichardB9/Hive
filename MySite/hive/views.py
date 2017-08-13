from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader


def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('hive/index.html')
    context = {
        'latest_question_list': ['this is a question1', 'question2'],
    }

    return HttpResponse(template.render(context, request))

def board(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('hive/board.html')
    context = {}

    return HttpResponse(template.render(context, request))