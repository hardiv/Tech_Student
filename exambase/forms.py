from django import forms
from exambase.utils import *


class CreateQuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['topic', 'exam', 'exam_position']

    highest_option = forms.CharField(max_length=1)
    correct_option = forms.CharField(max_length=1)


class QuestionAnswerForm(forms.Form):

    def __init__(self, *args, **kwargs):
        q_id = kwargs.pop('q_id')
        super(QuestionAnswerForm, self).__init__(*args, **kwargs)

        if q_id:
            self.fields['choice'].choices = get_choices(Question.objects.get(pk=q_id))

    choice = forms.ChoiceField()
