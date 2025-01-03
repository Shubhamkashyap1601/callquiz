from django.urls import path, include
from . import views


urlpatterns = [
    path('quizzes/', views.list_quizzes, name='list_quizzes'),
    path('<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('create/', views.create_quiz, name='create_quiz'),
    path('<int:quiz_id>/edit/', views.edit_quiz, name='edit_quiz'),
    path('<int:quiz_id>/delete/', views.delete_quiz, name='delete_quiz'),
    path('result/', views.save_result, name='save_result'),
    path('<int:quiz_id>/attempt/', views.attempt_quiz, name='attempt_quiz'),
    path('<int:quiz_id>/results/', views.quiz_results, name='quiz_results'),
     path('quiz/<int:quiz_id>/attempt/', views.attempt_quiz, name='attempt_quiz'),
     path('quiz/<int:quiz_id>/attempt/', views.quiz_detail, name='quiz_detail'),
     path('', views.home, name='home'),
     path('quiz/<int:quiz_id>/leaderboard/', views.quiz_leaderboard, name='quiz_leaderboard'),
]
