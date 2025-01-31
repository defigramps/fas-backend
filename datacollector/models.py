from django.db import models

class Curriculum(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.curriculum.name})"


class Topic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.subject.name})"


class Subtopic(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='subtopics')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.topic.name})"


class SubtopicContent(models.Model):
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE, related_name='contents')
    text = models.TextField(blank=True)
    video_url = models.URLField(blank=True, null=True)  # URL for YouTube video

    def __str__(self):
        return f"Content for {self.subtopic.name}"


class PracticeQuestion(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='practice_questions')
    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    option_e = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1)  # A, B, C, D, E
    explanation = models.TextField(blank=True)

    def __str__(self):
        return self.question


class PastQuestion(models.Model):
    YEARS = [(year, str(year)) for year in range(1998, 2025)]  # Predefined list of years

    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name='past_questions')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='past_questions')
    year = models.PositiveIntegerField(choices=YEARS)  # Add predefined year choices
    is_theory = models.BooleanField(default=False)
    question = models.TextField()
    option_a = models.CharField(max_length=255, blank=True, null=True)
    option_b = models.CharField(max_length=255, blank=True, null=True)
    option_c = models.CharField(max_length=255, blank=True, null=True)
    option_d = models.CharField(max_length=255, blank=True, null=True)
    option_e = models.CharField(max_length=255, blank=True, null=True)
    correct_option = models.CharField(max_length=255, blank=True, null=True)  # Increase length to 255
    explanation = models.TextField(blank=True, null=True)
    answer = models.TextField(blank=True, null=True)  # For theory questions

    def __str__(self):
        return f"{self.subject.name} ({self.year})"
