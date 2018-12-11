from django.db import models
from core.models import BaseModel, DBTestModel, DBRelativeModel
from testing.models import QuestionSet
import random, hashlib
from core import settings
from .forms import *
from django.contrib.auth.models import User


class TestData(BaseModel):
    """
        Contains user data from properly filled registration questionnaire,
        set of questions, generated for this user
        and answers on these questions from the user.
    """

    token = models.CharField(max_length=32, blank=True, null=True)

    create_date = models.DateTimeField(auto_now_add=True)
    finish_date = models.DateTimeField(blank=True, null=True)

    test_started = models.BooleanField(default=False)

    test_reviewed = models.BooleanField(default=False)

    # Personal Data Fields
    gender = models.CharField(max_length=20, choices=GENDER)
    age = models.PositiveIntegerField()
    education = models.CharField(max_length=20, choices=EDUCATION)
    activity_field = models.CharField(max_length=20, choices=ACTIVITY_FIELD)
    occupation = models.CharField(max_length=20, choices=OCCUPATION)
    economy_attitude = models.TextField()  # TODO: Add validation

    question_set = models.ForeignKey("testing.QuestionSet", models.CASCADE)

    @staticmethod
    def add_record(form: RegisterForm):
        """
        Generate new user record from valid form
        :param form: Filled-in RegisterForm
        :return: New user object if form is valid or None
        """
        if form.is_valid():
            new_user = TestData(**form.cleaned_data)

            # Randomly take one question set
            qs_count = QuestionSet.objects.count()
            qs_num = random.randint(0, qs_count - 1)
            qs_object = QuestionSet.objects.all()[qs_num]

            new_user.question_set = qs_object

            new_user.save()

            return new_user
        return None

    @staticmethod
    def get_test_instances():  # Not finished
        data = [
            # {
            #     'gender': GENDER_ENUM[0],
            #     'age': 24,
            #     'education': EDUCATION_ENUM[4],
            #     'activity_field': ACTIVITY_FIELD_ENUM[2],
            #     'occupation': OCCUPATION_ENUM[4],
            #     'economy_attitude': ECONOMY_ATTITUDE_ENUM[0] + ' ' + ECONOMY_ATTITUDE_ENUM[-1],
            #     'question_set': DBRelativeModel(QuestionSet, get_first=True),
            # }
        ]
        return [DBTestModel(__class__, **x) for x in data]

    def save(self, *args, **kwargs):
        super(TestData, self).save(*args, **kwargs)

        if not self.token:
            self.token = hashlib.md5((str(self.id) + settings.HASH_SALT).encode('utf-8')).hexdigest()
            super(TestData, self).save(update_fields=('token',), ignore_validation=True)

    def __str__(self):
        return str(self.gender) + " пол, Возраст: " + str(self.age) + ", " + str(self.education) + ", Вариант "\
               + str(self.question_set_id)


class Answer(BaseModel):
    """ Answer of a user for a question """

    CONTENT_TYPES = (
        ('text', 'text'),
        ('tex', 'TEX'),
    )

    user_data = models.ForeignKey("TestData", on_delete=models.CASCADE, related_name='answers')
    answer_option = models.ForeignKey("testing.Answer", on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField()
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES, default='text')
    is_right = models.NullBooleanField(default=None, blank=True, null=True)
