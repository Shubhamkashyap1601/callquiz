from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views import View
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .models import Quiz, Question, Option, QuizResult, Leaderboard
import logging
logger = logging.getLogger(__name__)
import traceback
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404


def home(request):
    quizzes = Quiz.objects.all()
    leaderboard_data = {}

    # For each quiz, get the leaderboard
    for quiz in quizzes:
        leaderboard = Leaderboard.objects.filter(quiz=quiz).order_by('-score')[:10]  # Top 10
        leaderboard_data[quiz] = leaderboard

    return render(request, 'quiz/home.html', {'quizzes': quizzes, 'leaderboard_data': leaderboard_data})


def list_quizzes(request):
    print("list_quizzes called")
    print("Traceback:")
    traceback.print_stack()
    print(f"list_quizzes called with path: {request.path} and query params: {request.GET}")
    
    quizzes = Quiz.objects.values('id', 'title', 'description')
    paginator = Paginator(quizzes, 5)  # Show 5 quizzes per page
    page_number = request.GET.get('page')
    print(f"Page number received: {page_number}")
    
    try:
        page_obj = paginator.get_page(page_number)
        quizzes_data = list(page_obj)
    except Exception as e:
        print(f"Error in pagination: {e}")
        return JsonResponse({"error": "Pagination issue"}, status=400)

    print(f"Returning quizzes data: {quizzes_data}")
    return JsonResponse({
        "quizzes": quizzes_data,
        "page": page_obj.number,
        "total_pages": paginator.num_pages
    })

def quiz_detail(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)

    if request.method == 'POST':
        # Assuming you're getting the score from a POST request (e.g., form submission)
        user = request.user  # Or fetch the user from the session if they aren't logged in
        score = request.POST.get('score')

        # Save the score to the leaderboard
        leaderboard_entry, created = Leaderboard.objects.get_or_create(user=user, quiz=quiz)
        leaderboard_entry.score = score
        leaderboard_entry.save()

        # After saving, redirect to avoid re-submission on refresh
        return redirect('home')

    leaderboard_data = {}
    quizzes = Quiz.objects.all()

    # For each quiz, get the leaderboard, sorted by score
    for quiz in quizzes:
        leaderboard = Leaderboard.objects.filter(quiz=quiz).order_by('-score')[:10]  # Get top 10 scores
        leaderboard_data[quiz] = leaderboard

    return render(request, 'quizapp/home.html', {'quizzes': quizzes, 'leaderboard_data': leaderboard_data})


def take_quiz(request, quiz_id):
    try:
        quiz = Quiz.objects.get(id=quiz_id)
    except Quiz.DoesNotExist:
        return JsonResponse({"error": "Quiz not found"}, status=404)
    
    questions = quiz.questions.all()
    questions_data = [
        {
            "question_id": question.id,
            "question_text": question.question_text,
            "options": [{"id": option.id, "text": option.option_text} for option in question.options.all()],
        }
        for question in questions
    ]
    
    return JsonResponse({"quiz_title": quiz.title, "questions": questions_data})


# Create Quiz
@csrf_exempt
@require_http_methods(["POST"])
@login_required
@user_passes_test(lambda user: user.is_staff)
def create_quiz(request):
    try:
        data = json.loads(request.body)
        quiz = Quiz.objects.create(title=data["title"], description=data["description"])
        
        for question_data in data["questions"]:
            question = Question.objects.create(quiz=quiz, question_text=question_data["question_text"], correct_answer=question_data["correct_answer"])
            
            for option_text in question_data["options"]:
                Option.objects.create(question=question, option_text=option_text)
        
        return JsonResponse({"message": "Quiz created successfully"})
    except KeyError as e:
        return JsonResponse({"error": f"Missing key: {e}"}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)


# Edit Quiz
@csrf_exempt
@require_http_methods(["POST"])
def edit_quiz(request, quiz_id):
    try:
        quiz = Quiz.objects.get(id=quiz_id)
        data = json.loads(request.body)
        
        quiz.title = data["title"]
        quiz.description = data["description"]
        quiz.save()

        for question_data in data["questions"]:
            question = Question.objects.get(id=question_data["id"], quiz=quiz)
            question.question_text = question_data["question_text"]
            question.correct_answer = question_data["correct_answer"]
            question.save()

            for option_text in question_data["options"]:
                Option.objects.create(question=question, option_text=option_text)

        return JsonResponse({"message": "Quiz updated successfully"})
    except Quiz.DoesNotExist:
        return JsonResponse({"error": "Quiz not found"}, status=404)
    except KeyError as e:
        return JsonResponse({"error": f"Missing key: {e}"}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)


# Delete Quiz
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_quiz(request, quiz_id):
    try:
        quiz = Quiz.objects.get(id=quiz_id)
        quiz.delete()
        return JsonResponse({"message": "Quiz deleted successfully"})
    except Quiz.DoesNotExist:
        return JsonResponse({"error": "Quiz not found"}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def save_result(request):
    try:
        data = json.loads(request.body)
        quiz = Quiz.objects.get(id=data["quiz_id"])
        user = request.user

        # Save to QuizResult
        result = QuizResult.objects.create(
            user=user,
            quiz=quiz,
            score=data["score"],
            questions_attempted=data["questions_attempted"],
            correct_answers=data["correct_answers"]
        )

        # Update Leaderboard
        leaderboard_entry, created = Leaderboard.objects.get_or_create(
            quiz=quiz,
            user_name=user.username,
            defaults={"score": data["score"]}
        )
        if not created:
            leaderboard_entry.score = max(leaderboard_entry.score, data["score"])
            leaderboard_entry.save()

        return JsonResponse({"message": "Quiz result saved successfully"})
    except Quiz.DoesNotExist:
        return JsonResponse({"error": "Quiz not found"}, status=404)
    except KeyError as e:
        return JsonResponse({"error": f"Missing key: {e}"}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)



def attempt_quiz(request, quiz_id):
    quiz_id = int(quiz_id)  # Ensure quiz_id is an integer
    quiz = Quiz.objects.get(id=quiz_id)
    questions = quiz.questions.all()  # Get all the questions for the quiz

    if request.method == 'POST':
        score = 0
        for question in questions:
            selected_answer = request.POST.get(str(question.id))  # Get the selected answer ID from the form
            print(f"Selected Answer for Question {question.id}: {selected_answer}")
            if selected_answer:
                # Use the correct_answer directly if it's already a string
                correct_answer = str(question.correct_answer) if question.correct_answer else None
                if correct_answer and selected_answer == correct_answer:
                    score += 1
            print(f"Correct Answer: {correct_answer}")

        # Get user_name from form or use logged-in user's username
        user_name = request.POST.get('user_name', request.user.username)

        # Create the leaderboard entry
        Leaderboard.objects.create(
            user_name=user_name,  # Ensure the user_name is passed correctly
            quiz=quiz,  # The quiz they attempted
            score=score  # The score they achieved
        )

        return redirect('home')

    return render(request, 'quiz/attempt_quiz.html', {'quiz': quiz, 'questions': questions})

def quiz_results(request, quiz_id):
    score = request.GET.get('score')
    quiz = Quiz.objects.get(id=quiz_id)
    return render(request, 'quiz/results.html', {'quiz': quiz, 'score': score})

def quiz_leaderboard(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    logger.debug(f"Quiz ID: {quiz_id}, Quiz Title: {quiz.title}")

    leaderboard = Leaderboard.objects.filter(quiz=quiz).order_by('-score')
    return render(request, 'quiz/quiz_leaderboard.html', {'quiz': quiz, 'leaderboard': leaderboard})





