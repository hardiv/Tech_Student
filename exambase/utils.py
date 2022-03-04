from django.db.models.query import QuerySet
from exambase.models import *
import os


def get_q_img_rel_path(qId):
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
    return rel_path


def get_q_image_path(qId):
    rel_path = get_q_img_rel_path(qId)
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


def save_attempt(q_id, form, user):
    attempt = "This question has not been attempted yet"
    curr_question = Question.objects.get(pk=q_id)
    attempt_num = get_no_of_attempts(curr_question, user)
    if attempt_num > 0:
        attempt = f"This question has been attempted {attempt_num} times"
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


def get_max_attempt_id(attempts):
    # return the maximum attempt id
    return attempts.latest('id').id


def get_last_n_attempts(n, filtered_attempts, max_id):
    min_id = max_id - n
    last_n_attempts = filtered_attempts.filter(pk__range=(min_id, max_id))
    return last_n_attempts


def get_no_of_attempts(question, user):
    attempts_made = get_attempts(user).filter(question=question)
    return len(attempts_made)


def q_attempted(question, attempts):
    attempts_for_question = attempts.filter(question=question)
    if len(attempts_for_question) == 0:
        return False
    return True


def get_polarised_topics(attempts, polarisation):
    if polarisation == 'strong':
        polarised_attempts = attempts.filter(is_correct=True)
    else:
        polarised_attempts = attempts.filter(is_correct=False)
    max_id = get_max_attempt_id(attempts)
    polarised_attempts = get_last_n_attempts(10, polarised_attempts, max_id)
    # Here 'polarised' means correct/incorrect or strong/weak
    polarised_counts = {}
    polarised_topics = {}

    for attempt in polarised_attempts:
        question = attempt.question
        topic = question.topic
        if topic in polarised_counts.keys():
            polarised_counts[topic] += 1
        else:
            polarised_counts[topic] = 1

    for topic in polarised_counts.keys():
        count = polarised_counts[topic]
        if count >= 3:
            polarised_topics[topic] = count
    return polarised_topics


def get_strong_topics(attempts):
    return get_polarised_topics(attempts, polarisation='strong')


def get_weak_topics(attempts):
    return get_polarised_topics(attempts, polarisation='weak')


def get_strong_and_weak_topics(attempts):
    strong_topics, weak_topics  = get_strong_topics(attempts), get_weak_topics(attempts)
    for topic in strong_topics.keys():
        if topic in weak_topics.keys():  # check if a strong topic has also been identified as weak
            strong_count = strong_topics[topic]
            weak_count = weak_topics[topic]
            if weak_count >= strong_count:  # The topic is more weak than strong
                del strong_topics[topic]
            else:
                del weak_topics[topic]
    return list(strong_topics.keys()), list(weak_topics.keys())


def is_q_exclusively_wrong(question, attempts):
    for attempt in attempts:
        attempt_q = attempt.question
        if attempt_q == question:
            if attempt.is_correct:
                return False
    return True


def recommend_questions(weak_topics_list, attempts):
    questions = []
    for topic in weak_topics_list:
        qs_to_add = Question.objects.filter(topic=topic)
        for q in qs_to_add:
            if not q_attempted(q, attempts):
                questions.append(q)
            if is_q_exclusively_wrong(q, attempts):
                questions.append(q)
    return questions


def test():
    print(get_letters_up_to("F"))


if __name__ == "__main__":
    test()
