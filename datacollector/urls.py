from django.urls import path
from . import views
urlpatterns = [
    path('curricula/', views.CurriculumListCreateView.as_view(), name='curricula'),
    path('subjects/<int:curriculum_id>/', views.SubjectListCreateView.as_view(), name='subjects'),
    path('topics/<int:subject_id>/', views.TopicListCreateView.as_view(), name='topics'),
    path('topics/<int:topic_id>/subtopics/', views.SubtopicListCreateView.as_view(), name='subtopics'),
    path('subtopics/<int:subtopic_id>/content/', views.SubtopicContentView.as_view(), name='subtopic_content'),
    path('topics/<int:topic_id>/questions/', views.PracticeQuestionView.as_view(), name='practice_questions'),
    path('past-questions/', views.PastQuestionView.as_view(), name='past_questions'),
    path('past-questions/subject/<int:subject_id>/', views.PastQuestionView.as_view(), name='past_questions_by_subject'),
    path('past-questions/curriculum/<int:curriculum_id>/', views.PastQuestionView.as_view(), name='past_questions_by_curriculum'),
    path('curricula/<int:curriculum_id>/subjects/<int:subject_id>/topics/', views.TopicsBySubjectAndCurriculumView.as_view(), name='topics_by_subject_and_curriculum'),
    path('curricula/<int:curriculum_id>/subjects/<int:subject_id>/topics/<int:topic_id>/subtopics/', views.SubtopicsByTopicSubjectAndCurriculumView.as_view(), name='subtopics_by_topic_subject_and_curriculum'),
]
