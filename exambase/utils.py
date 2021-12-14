from exambase.models import *
import os


def get_q_image_path(qId):
    q_obj = Question.objects.get(pk=qId)
    examId = q_obj.exam.id
    exam_obj = Exam.objects.get(pk=examId)
    year = exam_obj.year
    paper = exam_obj.paper
    pos = q_obj.exam_position
    rel_path = f"{paper.upper()}_{year}_{pos}.jpg"
    path = "exambase" + os.path.sep + "assets" + os.path.sep + rel_path
    return path
