from django.urls import path
from . import views

app_name = 'onlineJudge'
urlpatterns = [
    path('register/', views.register_request, name="register"),
    path('login/', views.login_request, name="login"),
    path('logout/', views.log_out, name="logout"),
    path('login/check/', views.login_check, name="login_check"),
    path('register/verify/', views.register_verify, name="register_verify"),

    path('', views.login_request, name="login"),
    path('problems/',views.problems, name='problems'),
    path('problem/<int:problem_id>/',views.problemDetails,name='problem_detail'),
    path('submit/<int:problem_id>/',views.problemSubmit,name="submit"),
    path('submit/<str:status>/', views.result,name="result"),
    path('problem/',views.problemSubmissions,name='submissions'),
]