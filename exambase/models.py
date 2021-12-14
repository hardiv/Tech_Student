from django.db import models
from django.contrib.auth.models import User


class Exam(models.Model):
    year = models.CharField(max_length=6, default='Sample')
    paper = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.paper} {self.year}"


class Topic(models.Model):
    topic = models.CharField(max_length=200)

    def __str__(self):
        return self.topic


# def generate_path(exam, position):
#     year = exam.year
#     name = exam.paper
#     return f"{name}_{year}_{position}"


class Question(models.Model):
    question_image_path = models.CharField(max_length=200)
    topic = models.ForeignKey("Topic", on_delete=models.CASCADE)
    exam = models.ForeignKey("Exam", on_delete=models.CASCADE)
    exam_position = models.PositiveIntegerField()

    def __str__(self):
        return self.question_image_path


class Option(models.Model):
    question = models.ForeignKey("Question", on_delete=models.CASCADE, related_name="options")
    option = models.CharField("Choice", max_length=50)
    position = models.IntegerField()
    is_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.option

    class Meta:
        unique_together = [
            # no duplicated option per question
            ("question", "option"),
            # no duplicated position per question
            ("question", "position")
        ]
        ordering = ("position",)


class Attempt(models.Model):
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    choice = models.ForeignKey("Option", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
