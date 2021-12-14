from django import forms
from .models import Question, Option


class CreateQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'topic',
            'exam',
            'exam_position',
        ]


class QuestionAnswerForm(forms.Form):
    q_obj = Question.objects.get(pk=1)
    options = Option.objects.filter(question=q_obj.id)
    choices = []
    choice = forms.ChoiceField(choices=choices)
