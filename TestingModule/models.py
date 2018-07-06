from django.db import models


class Education(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    text = models.TextField()


class ActivityField(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    text = models.TextField()


class Occupation(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    text = models.TextField()


class EconomyAttitude(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    text = models.TextField()


class UserData(models.Model):
    id = models.BigAutoField(primary_key=True)
    gender = models.CharField(max_length=6)
    age = models.PositiveIntegerField()
    education = models.ForeignKey("Education", models.CASCADE)
    activity_field = models.ForeignKey("ActivityField", models.CASCADE)
    occupation = models.ForeignKey("Occupation", models.CASCADE)
    economy_attitude = models.ForeignKey("EconomyAttitude", models.CASCADE)
    question_set_id = models.ForeignKey("QuestionSet", models.CASCADE)


class QuestionSet(models.Model):
    id = models.BigAutoField(primary_key=True)
    questions = models.ManyToManyField("Question")


class Question(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.TextField()
    answers_id = models.ForeignKey("AnswerVariant", models.CASCADE)


class AnswerVariant(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.TextField()
