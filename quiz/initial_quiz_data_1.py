from quiz.models import Quiz, Question

# Create the first quiz
quiz_1 = Quiz.objects.create(
    title="General Knowledge Quiz",
    description="Test your general knowledge with this quiz!"
)

# Updated questions and answers for the first quiz with actual correct answers
questions_1 = [
    {"question_text": "What is the capital of France?", "options": ["Berlin", "Madrid", "Paris", "Rome"], "correct_answer": "Paris"},
    {"question_text": "Who wrote 'Romeo and Juliet'?", "options": ["Shakespeare", "Dickens", "Hemingway", "Austen"], "correct_answer": "Shakespeare"},
    {"question_text": "Which planet is known as the Red Planet?", "options": ["Earth", "Mars", "Venus", "Jupiter"], "correct_answer": "Mars"},
    {"question_text": "Who discovered gravity?", "options": ["Newton", "Einstein", "Galileo", "Tesla"], "correct_answer": "Newton"},
    {"question_text": "What is the largest ocean on Earth?", "options": ["Atlantic", "Indian", "Arctic", "Pacific"], "correct_answer": "Pacific"},
    {"question_text": "What is the tallest mountain in the world?", "options": ["K2", "Mount Kilimanjaro", "Mount Everest", "Mount Fuji"], "correct_answer": "Mount Everest"},
    {"question_text": "Which is the smallest country in the world?", "options": ["Vatican City", "Monaco", "San Marino", "Liechtenstein"], "correct_answer": "Vatican City"},
    {"question_text": "What is the boiling point of water?", "options": ["90°C", "100°C", "110°C", "120°C"], "correct_answer": "100°C"},
    {"question_text": "Who painted the Mona Lisa?", "options": ["Da Vinci", "Picasso", "Van Gogh", "Rembrandt"], "correct_answer": "Da Vinci"},
    {"question_text": "What is the largest animal on Earth?", "options": ["Elephant", "Blue Whale", "Shark", "Giraffe"], "correct_answer": "Blue Whale"}
]

# Create the questions for quiz_1
for q in questions_1:
    Question.objects.create(
        quiz=quiz_1,
        question_text=q['question_text'],
        option_1=q['options'][0],
        option_2=q['options'][1],
        option_3=q['options'][2],
        option_4=q['options'][3],
        correct_answer=q['correct_answer']
    )
