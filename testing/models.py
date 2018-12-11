from django.db import models
from core.models import BaseModel, DBTestModel, DBRelativeModel


class QuestionSet(BaseModel):
    """ Represents a manually-made collection of questions """
    questions = models.ManyToManyField("Question", through='QuestionToSet')

    @staticmethod
    def get_test_instances():
        return [DBTestModel(__class__) for i in range(1)]

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return "Вариант " + self.id


class QuestionToSet(BaseModel):
    """ Many-to-many relation model """

    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    question_set = models.ForeignKey("QuestionSet", on_delete=models.CASCADE)
    index = models.PositiveSmallIntegerField()

    @staticmethod
    def get_test_instances():
        data = [
            {
                'question': DBRelativeModel(Question, index=0),
                'question_set': DBRelativeModel(QuestionSet, index=0),
                'index': i,
            }
            for i in range(10)
        ]
        return [DBTestModel(__class__, **item) for item in data]


    class Meta:
        unique_together = (('question_set', 'index'),)


class Question(BaseModel):
    """ Test question """

    CONTENT_TYPES = (
        ('text', 'text'),
        ('tex', 'TEX'),
    )

    content = models.TextField(verbose_name="Question content")
    image = models.ImageField(blank=True, null=True)
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES, default='text')

    @staticmethod
    def create_question(text, right_index, *answers):
        """ Create new text question with text answers """

        new_question = Question.objects.create(content=text)
        for index, answer in enumerate(answers):
            Answer(question=new_question, text=answer, index=index + 1, is_right=index == right_index).save()

        return new_question

    @property
    def is_open_question(self):
        if not self.answer_set.exists():
            return True
        return False

    @staticmethod
    def get_test_instances():
        data = [
            {'content': u'Сколько будет 2 + 2?'},
        ]
        return [DBTestModel(__class__, **item) for item in data]

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.content


class Answer(BaseModel):
    """ Answer for a question """

    CONTENT_TYPES = (
        ('text', 'text'),
        ('tex', 'TEX'),
    )

    question = models.ForeignKey("Question", models.CASCADE)
    is_right = models.BooleanField(default=False)
    text = models.TextField()
    index = models.PositiveSmallIntegerField()
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES, default='text')

    @staticmethod
    def get_test_instances():
        data = [
            {'question': DBRelativeModel(Question, index=0), 'text': '4', 'is_right': True, 'index': 1},
            {'question': DBRelativeModel(Question, index=0), 'text': '5', 'is_right': False, 'index': 2},
        ]
        return [DBTestModel(__class__, **item) for item in data]

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.text
