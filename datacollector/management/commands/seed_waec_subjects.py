import os
from django.core.management.base import BaseCommand
from datacollector.models import Curriculum, Subject

class Command(BaseCommand):
    help = 'Seed WAEC curriculum with subjects'

    def handle(self, *args, **kwargs):
        # Ensure the curriculum "WAEC" exists
        curriculum, created = Curriculum.objects.get_or_create(name='WAEC')

        # List of WAEC subjects
        subjects = [
            "COMMERCE",
            "FINANCIAL ACCOUNTING",
            "CHRISTIAN RELIGIOUS STUDIES",
            "ECONOMICS",
            "GEOGRAPHY",
            "GOVERNMENT",
            "HISTORY",
            "FURTHER MATHEMATICS"
            "LITERATURE IN ENGLISH",
            "CIVIC EDUCATION",
            "ENGLISH LANGUAGE",
            "GENERAL MATHEMATICS",
            "AGRICULTURAL SCIENCE",
            "BIOLOGY",
            "CHEMISTRY",
            "PHYSICS",
            "DATA PROCESSING",
            "HOME MANAGEMENT",
            "COMPUTER STUDIES",
        ]

        # Create subjects for WAEC curriculum
        for subject_name in subjects:
            Subject.objects.get_or_create(name=subject_name, curriculum=curriculum)

        self.stdout.write(self.style.SUCCESS('Successfully seeded WAEC subjects'))