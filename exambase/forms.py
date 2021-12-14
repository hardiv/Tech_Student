from django import forms
from .models import Question


class CreateQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'topic',
            'exam',
            'exam_position',
            'question_image_path'
        ]

