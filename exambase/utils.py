from django.db.models.query import QuerySet
from exambase.models import *
import os


def get_q_image_path(qId):
    q_obj = Question.objects.get(pk=qId)
    examId = q_obj.exam.id
    exam_obj = Exam.objects.get(pk=examId)
    year = exam_obj.year
    paper_name = exam_obj.paper_name
    paper_num = exam_obj.paper_num
    pos = q_obj.exam_position
    if paper_num is None:
        rel_path = f"{paper_name.upper()}_{year.replace(' ', '-')}_{pos}.jpg"
    else:
        rel_path = f"{paper_name.upper()}_{year}_P{paper_num}_{pos}.jpg"
    path = "exambase" + os.path.sep + "assets" + os.path.sep + rel_path
    return path


def get_paper_names():
    """
    :return: List of unique exam names that are currently stored in the database
    """
    exams = Exam.objects.all()
    names = set()
    for exam in exams:
        names.add(exam.paper_name)
    return names


def generate_url(q_id):
    question = Question.objects.get(pk=q_id)
    exam = question.exam
    url = f"{exam.paper_name}/{exam.year}-{exam.paper_num}/q{question.exam_position}".lower()
    # Convert the url all to lowercase so it stays consistent with the rest of the site
    return url


def save_attempt(q_id, form, user):
    attempt = "This question has not been attempted yet"
    option = None
    correctAns = None
    if form.is_valid():
        option_id = form.cleaned_data['choice']
        option = Option.objects.get(pk=option_id)
        if option.is_answer:
            correctAns = True
            print(f"{option} is Correct")
        else:
            correctAns = False
            print(f"{option} is Wrong")
        curr_question = Question.objects.get(pk=q_id)
        print(curr_question)
        attempt_num = get_no_of_attempts(curr_question, user) + 1
        attempt = Attempt(question=curr_question, choice=option, user=user, is_correct=correctAns,
                          num_attempts=attempt_num)
        attempt.save()
    return attempt, option, correctAns


def get_letters_up_to(letter):
    # Find the minimum and maximum ascii values
    min_ascii, max_ascii = ord("A"), ord(letter.upper())
    # Increment and add the characters denoted by each ASCII from min to max
    letters = [chr(ascii_val) for ascii_val in range(min_ascii, max_ascii+1)]
    return letters


def does_question_exist(topic, exam, pos):
    questions = Question.objects.filter(topic=topic).filter(exam=exam).filter(exam_position=pos)
    if not questions:
        # if no duplicate questions were found
        return False
    return True


def generate_options(form, question):
    highest_option = form.cleaned_data['highest_option']
    correct_option = form.cleaned_data['correct_option']
    # print(f"highest option: {highest_option}, correct: {correct_option}")
    option_names = get_letters_up_to(highest_option)
    for option_name in option_names:
        correct = False
        if option_name == correct_option:
            correct = True
        option = Option(question=question, option=option_name, is_answer=correct)
        option.save()


def get_choices(question):
    # Retrieves the options for the particular question
    options = Option.objects.filter(question=question)
    choices = []
    for option in options:
        # Populates tuple with the actual option object and its display name
        tup = (option.pk, f"Option {option.getOption()}")
        choices.append(tup)
    return choices


def get_attempts(user):
    return Attempt.objects.filter(user=user)


def get_no_of_attempts(question, user):
    attempts_made = get_attempts(user).filter(question=question)
    return len(attempts_made)


def progress_tracker(user):
    """
    :param user: current user object
    :return:
    """
    attempts = Attempt.objects.filter(user=user)
    incorrect_attempts = attempts.filter(is_correct=False)
    correct_attempts = attempts.filter(is_correct=True)
    pass


def test():
    print(get_letters_up_to("F"))


if __name__ == "__main__":
    test()
