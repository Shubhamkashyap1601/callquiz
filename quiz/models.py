# models.py

from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    time_limit = models.IntegerField(default=30)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()
    option_1 = models.CharField(max_length=255, default="")
    option_2 = models.CharField(max_length=255, default="")
    option_3 = models.CharField(max_length=255, default="")
    option_4 = models.CharField(max_length=255, default="")
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text


class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255)

    def __str__(self):
        return self.option_text

class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)
    questions_attempted = models.IntegerField()
    correct_answers = models.IntegerField()

    def __str__(self):
        return f"Result of {self.user} on {self.quiz.title}"
    
class Leaderboard(models.Model):
    user_name = models.CharField(max_length=255, default='Anonymous')  # Provide a default value
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.user_name} - {self.score}"

