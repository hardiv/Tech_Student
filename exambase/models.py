from django.db import models
from django.contrib.auth.models import User


class Exam(models.Model):
    year = models.CharField(max_length=15, default='Sample')
    paper_name = models.CharField(max_length=20)
    paper_num = models.IntegerField(null=True, blank=True)

    def getPaperNum(self):
        return f" P{self.paper_num}" if self.paper_num is not None else ""

    def __str__(self):
        return f"{self.paper_name} {self.year}{self.getPaperNum()}"


class Topic(models.Model):
    topic = models.CharField(max_length=200)

    def __str__(self):
        return self.topic


class Question(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    exam_position = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.exam}, Q{self.exam_position}"


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    option = models.CharField(max_length=1)
    is_answer = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question}, Option {self.option}"

    def getOption(self):
        return self.option

    class Meta:
        unique_together = [
            # no duplicated option per question
            ("question", "option"),
        ]


class Attempt(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Option, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    num_attempts = models.IntegerField(default=0)

    def __str__(self):
        if self.is_correct:
            return f"Correct - attempt no. {self.num_attempts} of {self.question}"
        else:
            return f"Wrong - attempt no. {self.num_attempts} of {self.question}"
