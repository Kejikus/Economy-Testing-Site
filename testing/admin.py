from django.contrib import admin
from django import forms
from . import models

admin.site.register(models.QuestionSet)
admin.site.register(models.Answer)

answer_fields = 5  # Number of answers in one question


class AddQuestionForm(forms.ModelForm):
    for i in range(1, answer_fields + 1):
        locals()['answer_%d' % i] = forms.CharField(label='Text for %i answer' % i)
    right_answer_number = forms.IntegerField(
            max_value=answer_fields, min_value=1,
            help_text='From %i to %i' % (1, answer_fields))

    class Meta:
        model = models.Question
        fields = ['content']

        def __init__(self):
            super(type(self), self).__init__()
            for i in range(1, answer_fields + 1):
                self.fields += ['answer_%i' % i]


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):

    def add_view(self, request, form_url='', extra_context=None):
        form_backup = self.form
        self.form = AddQuestionForm
        ret = super(QuestionAdmin, self).add_view(request, form_url, extra_context)
        self.form = form_backup
        return ret


del answer_fields
