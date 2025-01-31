import os
from django.core.management.base import BaseCommand
from datacollector.models import Curriculum, Subject, Topic, Subtopic

class Command(BaseCommand):
    help = 'Seed WAEC curriculum with subjects, topics, and subtopics'

    def handle(self, *args, **kwargs):
        # Ensure the curriculum "WAEC" exists
        curriculum, created = Curriculum.objects.get_or_create(name='WAEC')

        # List of WAEC subjects and their topics with subtopics
        subjects_data = {
            "GENERAL MATHEMATICS": {
                "Number and Numeration": [
                    "Number Bases: Conversion between different bases and basic operations in number bases.",
                    "Modular Arithmetic: Concepts and applications, including addition, subtraction, and multiplication in modulo arithmetic.",
                    "Fractions, Decimals, and Approximations: Operations on fractions and decimals, approximations, and significant figures.",
                    "Indices: Laws of indices and numbers in standard form (scientific notation).",
                    "Logarithms: Relationship between indices and logarithms, basic rules, and use of logarithm tables.",
                    "Sequences and Series: Patterns, arithmetic progression (A.P.), and geometric progression (G.P.).",
                    "Sets: Concepts of sets, including universal sets, subsets, and Venn diagrams.",
                    "Logical Reasoning: Statements, negations, implications, and use of symbols.",
                    "Positive and Negative Integers, Rational Numbers: Operations and representation on the number line.",
                    "Surds (Radicals): Simplification, rationalization, and basic operations involving surds.",
                    "Matrices and Determinants: Identification, operations, and determinants of matrices.",
                    "Ratio, Proportions, and Rates: Applications in financial partnerships, work rates, and more.",
                    "Percentages: Calculations involving interest, profit and loss, depreciation, and errors.",
                    "Financial Arithmetic: Topics like depreciation, annuities, and capital market instruments.",
                    "Variation: Direct, inverse, partial, and joint variations with practical applications."
                ],
                "Algebraic Processes": [
                    "Algebraic Expressions: Formulation and evaluation.",
                    "Operations on Algebraic Expressions: Expansion and factorization.",
                    "Solution of Linear Equations: Including simultaneous equations.",
                    "Change of Subject of a Formula/Relation: Rearranging formulas to solve for a specific variable."
                ],
                "Geometry and Trigonometry": [
                    "Plane Geometry: Properties of shapes, theorems, and constructions.",
                    "Mensuration: Measurement of lengths, areas, and volumes.",
                    "Coordinate Geometry: Equations of lines and curves, distances, and midpoints.",
                    "Trigonometry: Trigonometric ratios, identities, and equations."
                ],
                "Calculus": [
                    "Differentiation: Basic principles and applications.",
                    "Integration: Fundamental concepts and uses."
                ],
                "Statistics and Probability": [
                    "Data Presentation: Tables, charts, and graphs.",
                    "Measures of Central Tendency and Dispersion: Mean, median, mode, range, variance, and standard deviation.",
                    "Probability: Basic concepts and calculations."
                ]
            }
        }

        # Create subjects, topics, and subtopics for WAEC curriculum
        for subject_name, topics in subjects_data.items():
            subject, created = Subject.objects.get_or_create(name=subject_name, curriculum=curriculum)
            for topic_name, subtopics in topics.items():
                topic, created = Topic.objects.get_or_create(name=topic_name, subject=subject)
                for subtopic_name in subtopics:
                    Subtopic.objects.get_or_create(name=subtopic_name, topic=topic)

        self.stdout.write(self.style.SUCCESS('Successfully seeded WAEC subjects, topics, and subtopics'))