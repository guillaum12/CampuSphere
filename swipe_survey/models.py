from django.db import models
from profiles.models import Profile
from django.utils import timezone

# Create your models here.


class SwipeSurvey(models.Model):
    """
    Model to store swipe survey
    """
    survey_id = models.AutoField(primary_key=True)

    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    date_open = models.DateTimeField(null=True, default=None)
    date_close = models.DateTimeField(null=True, default=None)

    def __str__(self):
        return self.title

    @property
    def is_open(self):
        if self.date_open is None or self.date_close is None:
            return False

        return self.date_open < timezone.now() < self.date_close

    @property
    def number_of_questions(self):
        return SwipeQuestion.objects.filter(survey=self).count()

    @property
    def get_questions(self):
        return SwipeQuestion.objects.filter(survey=self).order_by('position')


class SwipeQuestion(models.Model):
    """
    Model to store swipe question
    """
    # Définition des types de questions possibles
    QUESTION_TYPES = [
        ("short", "Réponse courte"),
        ("long", "Réponse longue"),
        ("binary", "Question binaire"),
        ("multiple", "Choix multiple"),
        ("radio", "Choix unique"),
        ("scale", "Échelle")
    ]
    question_id = models.AutoField(primary_key=True)

    survey = models.ForeignKey(SwipeSurvey, on_delete=models.CASCADE)

    position = models.IntegerField()
    question = models.CharField(max_length=250)
    type = models.CharField(max_length=10, choices=QUESTION_TYPES)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['survey', 'position'], name='unique_position_in_survey')
        ]

    def __str__(self):
        return f"{self.survey} - [{self.position}] {self.question}"


class SwipePossibleAnswer(models.Model):
    """
    Model to store swipe possible answer
    """
    answer_id = models.AutoField(primary_key=True)

    question = models.ForeignKey(SwipeQuestion, on_delete=models.CASCADE)
    content = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def is_free_field(self):
        """Return True if the answer is a free field, False otherwise."""
        return self.content is None

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['question', 'content'],
                                    name='unique_possible_answer_in_question')
        ]

    @property
    def number_of_answers(self):
        return SwipeAnswerUser.objects.filter(answer=self).count()

    def __str__(self):
        dbt = f"Sondage {self.question.survey.survey_id} - [{self.question.question_id}] "
        if self.content is None:
            return f"{dbt}Champ d'expression libre"
        return dbt + self.content


class SwipeAnswerUser(models.Model):
    """
    Model to store swipe answer from profile
    """
    answer_user_id = models.AutoField(primary_key=True)

    answer = models.ForeignKey(SwipePossibleAnswer, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['answer', 'profile'], name='unique_answer_from_user'),
        ]

    def get_answer(self):
        if self.answer.is_free_field:
            return self.content
        return self.answer.content

    def __str__(self):
        if self.answer.is_free_field:
            return f"{self.profile} : {self.content}"
        return f"{self.profile} : {self.answer}"
