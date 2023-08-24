from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice, Vote
import json
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def index(request):
    lista_questions = Question.objects.all()

    # resultado = ", ".join([q.question_text for q in lista_questions])
    # return HttpResponse("<h1> Hello, world. Estas son las preguntas. \n </h1>" + resultado)

    contexto = {'latest_questions': lista_questions,
                'my_latest_questions': [],
                'saludo': 'Hello, world.'}

    if request.user.is_authenticated:
        contexto['saludo'] = 'Hello, world. Estas son tus encuestas ' + request.user.username
        contexto['latest_questions'] = lista_questions.exclude(author=request.user)
        contexto['my_latest_questions'] = lista_questions.filter(author=request.user)

    return render(request, "polls/index.html", contexto)


def questions(request):
    lista_questions = Question.objects.all()
    q_list = [{"id": q.id, "question_text": q.question_text,
            "pub_date": str(q.pub_date)} for  q in lista_questions]
    dict_questions = {'questions': q_list}
    return  HttpResponse(json.dumps(dict_questions), content_type='application/json')


@login_required
def details(request, question_id):
    #question = None
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("La encuesta no existe")

    if question.author == request.user:
        votes = question.vote_set.all().order_by('choice')
        return render(request, "polls/results.html", {'q': question,
                                                      'votes': votes})

    if Vote.objects.filter(user=request.user, question=question):
        return render(request, "polls/results.html", {'q': question})
    else:
        return render(request, "polls/detail.html", {'q': question})
    # return HttpResponse("Mostrando el detalle de la pregunta %s" % question_id)



def results(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("La encuesta no existe")

    return render(request, "polls/results.html", {'q': question})


@login_required
def vote(request, question_id):
    print(request.POST)
    question = Question.objects.get(pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(
                      request,
                      "polls/detail.html",
                      {
                         "q": question,
                         "error_message": "No seleccionaste una opcion."
                      }
                )

   # if request.session.get(str(question_id), False):
   #     return render(
   #                   request,
   #                   "polls/detail.html",
   #                   {
   #                      "q": question,
   #                      "error_message": "Ya votaste."
   #                   }
   #             )
   # else:
   #     request.session[str(question_id)] = True

    Vote.objects.create(user=request.user,question=question,choice=selected_choice)

    selected_choice.votes = selected_choice.votes+1
    selected_choice.save()
    return HttpResponseRedirect(reverse("results", args=(question_id,)))
    # return render(request,"polls/detail.html",{question: ques)


def results_update(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("La encuesta no existe")
    
    if question.author == request.user:
        votes = Vote.objects.filter(question=question)
        return render(request, "polls/results_update.html", {'q': question,
                                                             'vote': votes})
    else:
        return render(request, "polls/results_update.html", {'q': question})


@login_required
def add_question(request):
    # CSRF?
    if request.method == 'GET':
        return render(request, "polls/add_question.html", {'state': 'get'})
    elif request.method == 'POST':
        question = Question.objects.create(
            author=request.user,
            question_text=request.POST['question_text'],
            pub_date=timezone.now())
        return render(request, "polls/add_question.html", {'state': 'SUCCESS',
                                                           'q': question
                                                           })


@login_required
def add_choice(request, question_id):
    # CSRF?
    if request.method == 'GET':
        return render(request, "polls/add_choice.html", {'state': 'get'})
    elif request.method == 'POST':
        try:
            question = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            raise Http404("La encuesta no existe")
        choice = Choice.objects.create(
            question=question,
            choice_text=request.POST['choice_text'],
            votes=0)
        return render(request, "polls/add_choice.html", {'state': 'SUCCESS',
                                                           'c': choice
                                                           })
