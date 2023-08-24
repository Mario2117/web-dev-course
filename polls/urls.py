from django.urls import path 
from . import views

urlpatterns = [
        path("", views.index, name="index"),
        path("api/questions", views.questions, name="questions"),
        path("<int:question_id>/", views.details, name="details"),
        path("<int:question_id>/results/", views.results, name="results"),
        path("<int:question_id>/vote/", views.vote, name="vote"),
        path("<int:question_id>/results/update", views.results_update,
             name="results_update"),
        path("api/question/add", views.add_question, name="add_question"),
        path("<int:question_id>/api/choice/add", views.add_choice, name="add_choice"),]
