import json
import os
from django.core.management.base import BaseCommand
from datacollector.models import Curriculum, Subject, PastQuestion

class Command(BaseCommand):
    help = 'Seed questions from 2022MTHdata.json into the database'

    def handle(self, *args, **kwargs):
        file_path = os.path.join('seed', '2022MTHdata.json')
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return

        with open(file_path, 'r') as file:
            data = json.load(file)

        # Ensure the curriculum "JAMB" exists
        curriculum, created = Curriculum.objects.get_or_create(name='JAMB')

        # Ensure the subject exists (assuming a subject name, e.g., "Use of English")
        subject, created = Subject.objects.get_or_create(name='Mathematics', curriculum=curriculum)

        for item in data:
            question_text = item['question']
            option_a = item['option_a'].split('\r\n')[1].strip() if item['option_a'] else None
            option_b = item['option_b'].split('\r\n')[1].strip() if item['option_b'] else None
            option_c = item['option_c'].split('\r\n')[1].strip() if item['option_c'] else None
            option_d = item['option_d'].split('\r\n')[1].strip() if item['option_d'] else None
            option_e = item['option_e'].split('\r\n')[1].strip() if item['option_e'] else None
            correct_option = item['correct_option'].split(': ')[1].strip() if item['correct_option'] else None

            PastQuestion.objects.create(
                curriculum=curriculum,
                subject=subject,
                year=2022,
                question=question_text,
                option_a=option_a,
                option_b=option_b,
                option_c=option_c,
                option_d=option_d,
                option_e=option_e,
                correct_option=correct_option
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded questions from 2022MTHdata.json'))