from quiz.models import Quiz, Question

# Create the second quiz
quiz_2 = Quiz.objects.create(
    title="Science Quiz",
    description="A challenging science quiz to test your knowledge!"
)

# Updated questions and answers for the second quiz with actual correct answers
questions_2 = [
    {"question_text": "What is the chemical symbol for water?", "options": ["H2O", "CO2", "O2", "H2"], "correct_answer": "H2O"},
    {"question_text": "What planet is known as the Red Planet?", "options": ["Earth", "Mars", "Venus", "Jupiter"], "correct_answer": "Mars"},
    {"question_text": "What is the hardest natural substance?", "options": ["Gold", "Diamond", "Iron", "Platinum"], "correct_answer": "Diamond"},
    {"question_text": "Who developed the theory of relativity?", "options": ["Newton", "Einstein", "Bohr", "Darwin"], "correct_answer": "Einstein"},
    {"question_text": "What is the atomic number of hydrogen?", "options": ["1", "2", "3", "4"], "correct_answer": "1"},
    {"question_text": "What gas do plants absorb from the atmosphere?", "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"], "correct_answer": "Carbon Dioxide"},
    {"question_text": "How many bones are in the human body?", "options": ["206", "205", "204", "208"], "correct_answer": "206"},
    {"question_text": "What is the center of an atom called?", "options": ["Electron", "Proton", "Neutron", "Nucleus"], "correct_answer": "Nucleus"},
    {"question_text": "Which is the largest planet in our solar system?", "options": ["Mars", "Venus", "Jupiter", "Saturn"], "correct_answer": "Jupiter"},
    {"question_text": "What is the chemical formula for salt?", "options": ["NaCl", "H2O", "CO2", "O2"], "correct_answer": "NaCl"}
]

# Create the questions for quiz_2
for q in questions_2:
    Question.objects.create(
        quiz=quiz_2,
        question_text=q['question_text'],
        option_1=q['options'][0],
        option_2=q['options'][1],
        option_3=q['options'][2],
        option_4=q['options'][3],
        correct_answer=q['correct_answer']
    )

