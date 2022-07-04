import imp
from unicodedata import name
from django.urls import path
from . import views

app_name = 'onlineJudge'
urlpatterns = [
    path('',views.problems, name='problems'),
    path('problem/<int:problem_id>/',views.problemDetails,name='problem_detail'),
    path('problem/<int:problem_id>/submission',views.problemSubmission,name='submission'),
]